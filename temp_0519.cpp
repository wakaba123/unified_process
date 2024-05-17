#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <fcntl.h>
#include <dirent.h>
#include <regex>
#include <fstream>

struct process_information {
    std::string package_name;
    std::vector<pid_t> pids;
    std::vector<std::vector<pid_t>> all_tids;
    std::vector<std::vector<pid_t>> white_tids;
};

// 通过包名获得pid
std::vector<int> getPIDList(const std::string& packageName) {
    std::vector<int> pidList;
    std::string command = "pidof " + packageName;
    FILE* pipe = popen(command.c_str(), "r");
    if (!pipe) {
        std::cout << "Error executing pidof command." << std::endl;
        return pidList;
    }

    char buffer[128];
    while (fgets(buffer, sizeof(buffer), pipe) != nullptr) {
        std::istringstream iss(buffer);
        std::string pidStr;
        while (iss >> pidStr) {
            int pid = std::stoi(pidStr);
            pidList.push_back(pid);
        }
    }

    pclose(pipe);
    return pidList;
}

// 针对每一个pid都获得render thread 并加入数组中
std::vector<pid_t> get_render_thread(pid_t pid) {
    int fd = open("/dev/hisi_per_ctrl", O_RDWR);
    init_render_pid_demt(pid, fd);
    std::vector<int> render_tids = get_render_rt_demt(pid, fd);
    return render_tids;
}

std::vector<pid_t> getTIDList(pid_t pid) {
    std::vector<pid_t> tidList;
    std::regex tidRegex("\\d+");

    std::string procPath = "/proc/" + std::to_string(pid) + "/task";
    DIR* dir = opendir(procPath.c_str());
    if (!dir) {
        std::cout << "Error opening directory: " << procPath << std::endl;
        return tidList;
    }

    struct dirent* entry;
    while ((entry = readdir(dir)) != nullptr) {
        std::string entryName = entry->d_name;
        if (std::regex_match(entryName, tidRegex)) {
            pid_t tid = std::stoi(entryName);
            tidList.push_back(tid);
        }
    }

    closedir(dir);
    return tidList;
}

bool writeTargetToSchedDomain(pid_t pid, std::vector<pid_t>& tids, int target) {
    for (auto tid : tids) {
        std::string filePath = "/proc/" + std::to_string(pid) + "/task/" + std::to_string(tid) + "/sched_domain";
        std::ofstream file(filePath);
        if (!file) {
            std::cout << "Error opening file: " << filePath << std::endl;
            return false;
        }
        file << target;
        if (!file) {
            std::cout << "Error writing to file: " << filePath << std::endl;
            return false;
        }
        file.close();
    }
    return true;
}

void set_tid_sched_domain(std::vector<process_information> processes, int target) {
    for (auto process : processes) {
        std::vector<int> non_white_tids;
        for (int i = 0; i < processes.size(); i++) {
            std::set_difference(
                process.all_tids[i].begin(), process.all_tids[i].end(),
                process.white_tids[i].begin(), process.white_tids[i].end(),
                std::back_inserter(non_white_tids));
            writeTargetToSchedDomain(process.pids[i], non_white_tids, target);
        }
    }
}

struct process_information* get_process_information(std::string package_name) {
    struct process_information* temp = new struct process_information;
    temp->package_name = package_name;
    temp->pids = getPIDList(package_name);
    for (auto pid : temp->pids) {
        temp->all_tids.push_back(getTIDList(pid));
        temp->white_tids.push_back(get_render_thread(pid));
    }
    return temp;
}

std::string foreground_app = "com.qiyi.hmy";
std::string background_app = "com.huawei.broswer";

int main() {
    struct process_information* fore = get_process_information(foreground_app);
    struct process_information* back = get_process_information(background_app);
    std::vector<struct process_information> processes = {fore, back};
    set_tid_sched_domain(processes, 1);
    return 0;
}