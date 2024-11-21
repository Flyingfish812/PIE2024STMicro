Data processing:

I directly used Adam's data processing results. For detailed information about the data, please refer to the file data_all.xlsx. 
Below are some key points:
1. To address the issue of imbalance across different categories, Adam adopted the approach of oversampling the underrepresented categories and downsampling the overrepresented ones. I think this is quite reasonable.
2. Regarding the labels, Adam added Gaussian noise to the labels, converting categories A, B, C... into numerical values. I think there are some problems in this process. For example, the mean values of the Gaussian distributions for B/Upgrade and B/Downgrade should not differ because, by definition, ~/Upgrade and ~/Downgrade do not represent differences in similarity.
3. I don't quite understand why Adam removed categories D and SF.

For the model input, I applied one-hot encoding to the Supplier_Package values and then concatenated the two samples directly as the model input. However, I believe there might be a better approach.

Model：

Two commonly used libraries in Python:

Scikit-learn:
Scikit-learn is a widely used library for traditional machine learning methods. 
Scikit-learn is ideal for those working with traditional machine learning problems, particularly for tasks that don't involve deep learning.

PyTorch:
PyTorch is an open-source machine learning library primarily used for deep learning applications.

Differences:
1. Focus: Scikit-learn is focused on traditional machine learning algorithms, while PyTorch is geared towards deep learning.
2. Complexity: Scikit-learn is easier to use and provides high-level abstractions for standard machine learning tasks, whereas PyTorch offers low-level control over model architectures and computations.

My idea is to first use Scikit-learn to explore some traditional machine learning methods, and then use Pytroch to build more complex machine learning models. On the one hand, we can deepen our understanding of the problem and the data by applying traditional machine learning methods; on the other hand, when we fully understand the characteristics of the data and the problem, we can use Pytroch to build more complex and targeted models. 

The test results of various machine learning models (Random Forest, SVR...) can be found in the code file FirstTry.ipynb. Random forests seem to perform best.

Questions:
1. Regarding the problem that the number of samples in category A is too small, is it possible to record the similarity of two completely identical components as A, so as to increase the number of samples in category A?
2. Are there more specific evaluation criteria for the quality of the model?