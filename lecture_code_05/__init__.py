"""
1、建立自己的特征库(feature extracting)，把自己能想到的各种特征全部整合进特征库里，在需要的时候，将自己的特征库导入进来即可
特征库整合为FeatureUtils.py
when in use, just
import FeatureUtils

2、建立完训练特征库后，下一步建立训练数据集
即：将训练指标转换为可训练的数据集

3、脏活累活：将原始的金融数据集转换为新的训练数据集
-->raw data transfer to new training data

4、比较好的量化模型的feature数量依次为20，50，300（为经验数据）
20为一个坎，50为一个坎，300为一个坎

5、集成学习（只会提升效果）

决策树-->随机森林（集成学习的一种实现方法）
xgboost  GBDTs(老中医)

集成学习两种方法
blending stacking



"""