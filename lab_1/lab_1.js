// Загрузка OpenCV.js
let script = document.createElement('script');
script.setAttribute('src', 'https://docs.opencv.org/4.5.4/opencv.js');
script.onload = () => {
    // Функция для отображения изображения и его гистограммы
    function displayImageAndHistogram(image, grayscale, channels, histograms) {
        // Отображение изображения и его гистограммы
        cv.imshow('image', image);
        cv.imshow('grayscale', grayscale);
        for (let i = 0; i < channels.length; i++) {
            cv.imshow('channel' + i, channels[i]);
            cv.imshow('histogram' + i, histograms[i]);
        }
        // Ожидание нажатия клавиши
        cv.waitKey(0);
    }

    let img = new Image();
    img.src = 'image.png';

    let originalCanvas = document.getElementById('originalCanvas');
    let ctxOriginal = originalCanvas.getContext('2d');
    ctxOriginal.drawImage(img, 0, 0);

    let src = cv.imread('originalCanvas');

    let grayscale = new cv.Mat();
    cv.cvtColor(src, grayscale, cv.COLOR_BGR2GRAY);

    let channels = [];
    for (let i = 0; i < src.channels(); i++) {
        let channel = new cv.Mat();
        cv.split(src, channel);
        channels.push(channel);
    }

    // Вычисление гистограммы яркости для каждого канала
    let histograms = [];
    let histSize = 256;
    let histRange = [0, 256];
    let accumulate = false;
    for (let i = 0; i < channels.length; i++) {
        let hist = new cv.Mat();
        cv.calcHist([channels[i]], [0], new cv.Mat(), hist, [histSize], [histRange], accumulate);
        histograms.push(hist);
    }

    // Отображение изображения и его гистограммы
    displayImageAndHistogram(src, grayscale, channels, histograms);

    // Освобождение ресурсов
    src.delete();
    grayscale.delete();
    channels.forEach(channel => channel.delete());
    histograms.forEach(hist => hist.delete());
};
document.body.appendChild(script);
