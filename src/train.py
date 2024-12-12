import pandas as pd
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import torch
import torch.nn as nn
from tqdm import tqdm

current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file_path)
home = os.path.dirname(current_dir)

# Step 1: 配置属性信息
# 用户需要根据数据集修改此字典。
attribute_config = {
    "numerical": [
       'Maximum Input Offset Voltage',
       'Maximum Single Supply Voltage',
       'Minimum Single Supply Voltage',
       'Number of Channels per Chip',
       'Typical Gain Bandwidth Product',
       'Maximum Input Offset Voltage_comp',
       'Maximum Single Supply Voltage_comp',
       'Minimum Single Supply Voltage_comp',
       'Number of Channels per Chip_comp',
       'Typical Gain Bandwidth Product_comp'],  # 数字属性列名
    "categorical": ['Supplier_Package', 'Supplier_Package_comp']                      # 类别属性列名
}

# 嵌入维度
EMBEDDING_DIM = 16

# Step 2: 定义模型
class CombinedModel(nn.Module):
    def __init__(self, num_categories, embedding_dim, num_numerical_features):
        super(CombinedModel, self).__init__()
        self.embedding = nn.Embedding(num_categories, embedding_dim)  # 类别嵌入
        self.fc = nn.Sequential(
            nn.Linear(num_numerical_features + embedding_dim * 2, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )

    def forward(self, numerical_features, categorical_features):
        cat_embeds = [self.embedding(cat) for cat in categorical_features]
        cat_embeds = torch.cat(cat_embeds, dim=1)  # 拼接类别嵌入
        combined_features = torch.cat([numerical_features, cat_embeds], dim=1)
        output = self.fc(combined_features)
        return output

# Step 3: 数据处理

def preprocess_data(file_path):
    # 读取数据
    df = pd.read_csv(file_path)

    # 提取数值和类别属性
    numerical_data = df[attribute_config["numerical"]].values
    categorical_data = df[attribute_config["categorical"]]

    # 为类别属性生成唯一编号
    category_mappings = {}
    for col in attribute_config["categorical"]:
        category_mappings[col] = {value: idx for idx, value in enumerate(categorical_data[col].unique())}
        categorical_data[col] = categorical_data[col].map(category_mappings[col])

    categorical_data = categorical_data.values

    # 提取目标值 (最后一列默认是目标值，用户可修改)
    target = df.iloc[:, -1].values

    return numerical_data, categorical_data, target, category_mappings

# Step 4: 训练和验证

def train_and_evaluate(train_file):
    # 数据预处理
    numerical_data, categorical_data, target, category_mappings = preprocess_data(train_file)

    # 数据集划分
    X_train_num, X_test_num, X_train_cat, X_test_cat, y_train, y_test = train_test_split(
        numerical_data, categorical_data, target, test_size=0.1, random_state=42
    )

    # 转换为 PyTorch 张量
    X_train_num = torch.tensor(X_train_num, dtype=torch.float32)
    X_test_num = torch.tensor(X_test_num, dtype=torch.float32)
    X_train_cat = [torch.tensor(X_train_cat[:, i], dtype=torch.long) for i in range(X_train_cat.shape[1])]
    X_test_cat = [torch.tensor(X_test_cat[:, i], dtype=torch.long) for i in range(X_test_cat.shape[1])]
    y_train = torch.tensor(y_train, dtype=torch.float32).view(-1, 1)
    y_test = torch.tensor(y_test, dtype=torch.float32).view(-1, 1)

    # 定义模型
    num_categories = max(max(mapping.values()) for mapping in category_mappings.values()) + 1
    model = CombinedModel(num_categories=num_categories, embedding_dim=EMBEDDING_DIM, num_numerical_features=numerical_data.shape[1])

    # 损失函数和优化器
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    # 训练模型
    model.train()
    for epoch in tqdm(range(10)):  # 默认 10 个 epoch，用户可调整
        optimizer.zero_grad()
        outputs = model(X_train_num, X_train_cat)
        loss = criterion(outputs, y_train)
        loss.backward()
        optimizer.step()
        print(f"Epoch {epoch+1}, Loss: {loss.item()}")

    # 验证模型
    model.eval()
    with torch.no_grad():
        predictions = model(X_test_num, X_test_cat)
        test_loss = criterion(predictions, y_test)
        print(f"Test Loss: {test_loss.item()}")

if __name__ == "__main__":
    train_file_path = f'{home}\encoded data\input-data.csv'
    train_and_evaluate(train_file_path)
