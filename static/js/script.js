document.addEventListener('DOMContentLoaded', function () {
            const hamburger = document.querySelector('.hamburger');
            const menuMobile = document.querySelector('.menu-mobile');

            hamburger.addEventListener('click', () => {
                menuMobile.classList.toggle('active');
            });

            // Redimensionnement de la fenêtre
            window.addEventListener('resize', function () {
                if (window.innerWidth > 768) {
                    // Si la fenêtre devient plus large que 768px, cache le menu mobile et affiche le menu classique
                    menuMobile.classList.remove('active');
                }
            });
        });


