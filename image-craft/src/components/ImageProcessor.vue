<template>
  <div>
    <input type="file" @change="onFileChange">
    <canvas ref="canvas" @mousemove="onMouseMove"></canvas>
    <div v-if="pixelInfo" class="pixel-info">
      <p>Координаты: ({{ pixelInfo.x }}, {{ pixelInfo.y }})</p>
      <p>RGB: {{ pixelInfo.rgb }}</p>
      <p>Интенсивность: {{ pixelInfo.intensity.toFixed(2) }}</p>
      <p>Среднее (RGB): {{ pixelInfo.avg.toFixed(2) }}</p>
      <p>Стандартное отклонение (RGB): {{ pixelInfo.stdDev.toFixed(2) }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ImageProcessor',
  data() {
    return {
      pixelInfo: null,
      originalImage: null,
      charts: [],
    };
  },
  methods: {
    onFileChange(e) {
      const file = e.target.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = (e) => {
        const img = new Image();
        img.onload = () => {
          this.originalImage = img; // Установка после загрузки изображения
          this.drawImage(this.originalImage); // Передаем объект Image
        };
        img.src = e.target.result;
      };
      reader.readAsDataURL(file);
    },
    drawImage(img) {
      const canvas = this.$refs.canvas;
      canvas.width = img.width;
      canvas.height = img.height;
      const ctx = canvas.getContext('2d');
      ctx.drawImage(img, 0, 0); // Теперь img гарантированно является объектом Image
    },
    onMouseMove(e) {
      const rect = this.$refs.canvas.getBoundingClientRect();
      const x = Math.floor(e.clientX - rect.left);
      const y = Math.floor(e.clientY - rect.top);
      this.processPixelInfo(x, y);
      this.drawBorder(x, y);
    },
    processPixelInfo(x, y) {
      const ctx = this.$refs.canvas.getContext('2d');
      const imageData = ctx.getImageData(x-5, y-5, 11, 11).data;
      let rSum = 0, gSum = 0, bSum = 0, count = 0;
      let rValues = [], gValues = [], bValues = [];

      for (let i = 0; i < imageData.length; i += 4) {
        let r = imageData[i];
        let g = imageData[i + 1];
        let b = imageData[i + 2];
        rSum += r;
        gSum += g;
        bSum += b;
        rValues.push(r);
        gValues.push(g);
        bValues.push(b);
        count++;
      }

      const avgR = rSum / count;
      const avgG = gSum / count;
      const avgB = bSum / count;
      const avg = (avgR + avgG + avgB) / 3;

      const stdDevR = Math.sqrt(rValues.reduce((acc, val) => acc + Math.pow(val - avgR, 2), 0) / count);
      const stdDevG = Math.sqrt(gValues.reduce((acc, val) => acc + Math.pow(val - avgG, 2), 0) / count);
      const stdDevB = Math.sqrt(bValues.reduce((acc, val) => acc + Math.pow(val - avgB, 2), 0) / count);
      const stdDev = (stdDevR + stdDevG + stdDevB) / 3;

      const intensity = 0.299 * avgR + 0.587 * avgG + 0.114 * avgB;

      this.pixelInfo = {
        x: x,
        y: y,
        rgb: `rgb(${avgR.toFixed(0)}, ${avgG.toFixed(0)}, ${avgB.toFixed(0)})`,
        intensity: intensity,
        avg: avg,
        stdDev: stdDev
      };
    },
    drawBorder(x, y) {
      if (this.originalImage instanceof Image) {
        const ctx = this.$refs.canvas.getContext('2d');
        ctx.clearRect(0, 0, this.$refs.canvas.width, this.$refs.canvas.height); // Очистка предыдущего состояния
        ctx.drawImage(this.originalImage, 0, 0);
        ctx.strokeStyle = '#FF0000'; // Цвет рамки
        // Далее код рисования рамки
        const startX = Math.max(0, x - 5);
        const startY = Math.max(0, y - 5);
        const endX = Math.min(this.originalImage.width, x + 6);
        const endY = Math.min(this.originalImage.height, y + 6);
        ctx.strokeRect(startX, startY, endX - startX, endY - startY);
      }
    },
  }
}
</script>

<style>
.pixel-info {
  position: fixed;
  bottom: 0;
  background-color: rgba(255, 255, 255, 0.8);
  padding: 10px;
  border: 1px solid #ddd;
  font-size: 14px;
}
</style>
