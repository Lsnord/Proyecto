document.addEventListener('DOMContentLoaded', function () {
    var images = [
        '{% static "index-imgs/slider1.jpg" %}',
        '{% static "index-imgs/slider2.jpg" %}',
        '{% static "index-imgs/slider3.jpg" %}',
        '{% static "index-imgs/slider4.jpg" %}',
        '{% static "index-imgs/slider5.jpg" %}',
        '{% static "index-imgs/slider6.jpg" %}',
        '{% static "index-imgs/slider7.jpg" %}',
        '{% static "index-imgs/slider8.jpg" %}'
    ];
    var currentIndex = 0;
    var body = document.body;

    function changeBackground() {
        body.style.backgroundImage = 'url(' + images[currentIndex] + ')';
        currentIndex = (currentIndex + 1) % images.length;
    }

    // Cambiar la imagen cada 8 segundos
    setInterval(changeBackground, 6000);

    // Cambiar la imagen al cargar la página
    changeBackground();
});
