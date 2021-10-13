# Receipt-Digitalizer

Since sharing your household can be difficult when splitting the cost of shopping, I developed a CNN based model to help digitalize receipts when shopping. The model is build in a way, that it could predict in real time on a mobile device. By using Tensorflow as the backend, the model could easily be implemented in a mobile app. When using OCR (e.g. Tesseract), the receipt could even be fully digitalized.

# How it works

The model consists of a bounding box regression, which means that it will predict the coordinates of the four corners of a receipt. It is based upon the paper "Real-time Document Localization in Natural Images by Recursive Application of a CNN" by Khurram Javed and uses a recursive prediction to refine the corners of a receipt.

# Results
![alt text](https://github.com/schmid-sebastian/Receipt-Digitalizer/blob/main/result3.jpg?raw=true)

While the results look promising, the data at hand is actually the real problem here: Receipts are often wrinkled, which makes the prediction of a corner very hard. Sometimes, there are more than 4 corners, since the receipt is of such bad quality. Such cases are currently very hard for the model.
