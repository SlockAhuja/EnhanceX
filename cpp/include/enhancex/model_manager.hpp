#ifndef ENHANCEX_MODEL_MANAGER_HPP
#define ENHANCEX_MODEL_MANAGER_HPP

#include <string>
#include <unordered_map>
#include <iostream>

namespace enhancex {

class ModelManager {
public:
    ModelManager() = default;

    bool loadModel(const std::string& modelName, const std::string& path) {
        models_[modelName] = path;
        std::cout << "[EnhanceX C++ Engine] Loaded Model: " << modelName << " -> " << path << "\n";
        return true;
    }

    std::string getModelPath(const std::string& modelName) const {
        auto it = models_.find(modelName);
        if (it != models_.end()) {
            return it->second;
        }
        return "";
    }

private:
    std::unordered_map<std::string, std::string> models_;
};

} // namespace enhancex

#endif // ENHANCEX_MODEL_MANAGER_HPP
