# Traffic-sign-recognition-for-speed-regulation-in-urban-areas
This project explores the use of machine learning to improve the comfort and safety of autonomous vehicles through traffic sign recognition and obstacle detection.

This project explores the use of machine learning to improve the comfort and safety of autonomous vehicles through traffic sign recognition and obstacle detection.

Autonomous driving requires reliable perception of the environment. While sensors and cameras provide high-quality inputs, recognition remains challenging due to lighting variations (shadows, reflections, glare), distortions, and rotation of signs. Traffic signs, however, are standardized in shape and color, making them suitable for detection and classification tasks.

# Approach

Sign Extraction – Using techniques such as the Hough transform to detect geometric shapes (e.g., circles for speed limit signs).

Classification (k-Nearest Neighbors) – Comparing RGB pixel values of extracted signs against a labeled database, with performance evaluated through confusion matrices and accuracy metrics.

Comparison with Scikit-learn – Leveraging existing ML libraries to benchmark the KNN method.

Neural Networks (CNNs) – Extending recognition to obstacles and complex objects (e.g., pedestrians, vehicles), enabling real-time decision-making in diverse urban scenarios.

# Objectives

Detect and isolate traffic signs from dashcam video.

Identify the type of sign using supervised ML (KNN).

Validate results with Scikit-learn implementations.

Implement a convolutional neural network for obstacle detection beyond standardized signs.

Integrate recognition output with vehicle control logic (e.g., speed regulation or emergency braking).

# Impact

By combining traditional algorithms and deep learning, this work highlights the potential of embedded image recognition systems to assist autonomous driving. The ultimate goal is to enable vehicles to adapt their speed dynamically in cities, reducing risks and enhancing passenger comfort.
