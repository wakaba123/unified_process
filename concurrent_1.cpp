/*
 * @Author: wakaba blues243134@gmail.com
 * @Date: 2024-03-25 17:08:32
 * @LastEditors: wakaba blues243134@gmail.com
 * @LastEditTime: 2024-03-26 10:49:46
 * @FilePath: /scripts/concurrent_1.cpp
 * @Description: 
 * 
 * Copyright (c) 2024 by wakaba All Rights Reserved. 
 */
#include <iostream>
#include <thread>
#include <chrono>
#include <vector>
#include <string>
#include <cstdlib>

void execute(const std::string& cmd) {
    std::string fullCmd = "adb shell '" + cmd + "'";
    std::cout << fullCmd << std::endl;
    system(fullCmd.c_str());
}

void execute_in_thread(const std::string& command) {
    auto t1 = std::chrono::high_resolution_clock::now();
    execute(command);
    auto t2 = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> duration = t2 - t1;
    std::cout << "Execution time for command '" << command << "': " << duration.count() << " seconds\n";
}

int main(int argc, char* argv[]) {
    int num_threads = atoi(argv[1]);
    std::string command = "taskset 70 /data/local/tmp/label_image -m /data/local/tmp/tflite_model/inception_v4.tflite --count=200 --use_gpu=true";
    std::string command2 = "taskset 70 /data/local/tmp/label_image -m /data/local/tmp/tflite_model/inception_v4.tflite --count=200 --use_gpu=true";

    std::vector<std::thread> threads;
    auto t1 = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < num_threads; ++i) {
        threads.emplace_back(std::thread(execute_in_thread, command));
        // threads.emplace_back(std::thread(execute_in_thread, command2));
    }

    for (auto& thread : threads) {
        thread.join();
    }

    auto t2 = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> duration = t2 - t1;
    std::cout << duration.count() << " seconds\n";

    return 0;
}
