/*global $, jQuery, alert*/
(function($) {
    "use strict";

    function heroContentSlider() {
        var heroContSlider = $('.hero-content-slider'),
            autoplay = heroContSlider.data('autoplay'),
            autoplaySpeed = heroContSlider.data('speed');
        if ($(window).width() > 992) {
            heroContSlider.owlCarousel({
                animateOut: 'bounceOut',
                animateIn: 'bounceIn',
                autoplay: autoplay,
                autoplayTimeout: autoplaySpeed,
                items: 1,
                dots: false,
                mouseDrag: false,
                touchDrag: false,
                loop: true
            });
        } else {
            heroContSlider.owlCarousel({
                autoplay: false,
                items: 1,
                dots: false,
                mouseDrag: true,
                touchDrag: true,
                loop: true,
                autoHeight: true
            });
        }
    }

    function heroContentSliderFade() {
        $('.hero-content-slider').css({ 'opacity': '1' })
    }

    function heroSliderOwl() {
        var heroOwlSlider = $(".hero-slider"),
            autoplay = heroOwlSlider.data('autoplay'),
            autoplaySpeed = heroOwlSlider.data('speed'),
            touchSlide = heroOwlSlider.data('touch-drag');
        heroOwlSlider.owlCarousel({
            autoplay: autoplay,
            autoplayTimeout: autoplaySpeed,
            items: 1,
            mouseDrag: touchSlide,
            touchDrag: touchSlide,
            dots: false,
            nav: true,
            navSpeed: 500,
            loop: true,
            autoHeight: true,
            navText: ["<img src='img/assets/slider-left-thin-arrow.png'>", "<img src='img/assets/slider-right-thin-arrow.png'>"]
        });
        if ($('.hero-fullscreen>div').hasClass('hero-slider')) {
            $('.hero-fullscreen').css({ 'padding': '0' });
        }
    }

    function vossenIframes() {
        $('.video-container').click(function() {
            $(this).addClass('reveal');
            var videoImg = $(this).find('img'),
                videoIframe = $(this).find('iframe'),
                videoAttr = videoIframe.attr('data-video-embed'),
                videoPlay = videoAttr + "?autoplay=1&autoplay=true";
            videoImg.animate({ 'opacity': 0 }, 300);
            videoIframe.css('visibility', 'visible').attr('src', videoPlay);
            videoIframe[0].setAttribute('allowFullScreen', '');
        });
    }

    function sliderOwl() {
        var owlSlider = $(".carousel"),
            autoplay = owlSlider.data('autoplay'),
            autoplaySpeed = owlSlider.data('speed'),
            touchSlide = owlSlider.data('touch-drag'),
            loopSlides = owlSlider.data('loop');
        owlSlider.owlCarousel({
            autoplay: autoplay,
            autoplayTimeout: autoplaySpeed,
            items: 1,
            mouseDrag: touchSlide,
            touchDrag: touchSlide,
            dots: true,
            nav: true,
            loop: loopSlides,
            autoHeight: true,
            navText: ["<img src='img/assets/slider-left-thin-arrow.png'>", "<img src='img/assets/slider-right-thin-arrow.png'>"],
            navRewind: true,
            slideBy: 'page'
        });
    }

    function progressBars() {
        function progressBar() {
            $('.progress').each(function() {
                $(this).find('.progress-bar').animate({
                    width: $(this).attr('data-percent')
                }, 800);
            });
        }
        if ($('.progress-bars').data('animate-on-scroll') === 'on') {
            $('.progress-bars').waypoint(function() {
                progressBar();
            }, { offset: '100%', triggerOnce: true });
        } else {
            progressBar();
        }
    }

    function teamSlider() {
        $(".team-slider").owlCarousel({
            autoplay: false,
            items: 3,
            dots: true,
            responsiveRefreshRate: 200,
            responsive: {
                0: {
                    items: 1
                },
                600: {
                    items: 2
                },
                1200: {
                    items: 3
                }
            }
        });
    }

    $(window).resize(function() {
        setTimeout(function() {
            $('.vossen-portfolio-filters .active').trigger('click');
        }, 600);
    });

    function clientsSlider() {
        var clientSlider = $(".clients-slider"),
            autoplay = clientSlider.data('autoplay'),
            autoplaySpeed = clientSlider.data('speed');
        clientSlider.owlCarousel({
            autoplay: autoplay,
            autoplayTimeout: autoplaySpeed,
            loop: false,
            dots: false,
            nav: false,
            responsiveRefreshRate: 200,
            responsive: {
                0: {
                    items: 2
                },
                600: {
                    items: 5
                },
                1200: {
                    items: 6
                }
            }
        });
    }

    function vosMap() {
        $('#vossen-map').waypoint(function() {
            initVossenMaps()
        }, { offset: '100%', triggerOnce: true });
    }

    function vossenHeader() {
        $('.nav li.dropdown>a, .dropdown-submenu>a').on('click', function() {
            $(this).closest('.dropdown').siblings().removeClass('open');
            $(this).closest('.dropdown').toggleClass('open');
            return false;
        });
        $('.nav li a, .btn-scroll').on('click', function() {
            var $anchor = $(this);

            function scrollToAnchor() {
                $('html, body').stop().animate({
                    scrollTop: $($anchor.attr('href')).offset().top - offsetVar
                }, 1000, 'easeInOutExpo');
                event.preventDefault();
            }
            if ($(window).width() > 992) {
                var offsetVar = '59';
                scrollToAnchor();
            } else {
                var offsetVar = '0';
                scrollToAnchor();
            }
        });

        function navSmall() {
            $(window).scroll(function() {
                if ($(window).scrollTop() > 70) {
                    $('nav').addClass("nav-small");
                } else {
                    $('nav').removeClass("nav-small");
                }
            });
        }
        if ($('nav').data('animation') === 'hiding') {
            var vosWindow = $(window);
            var navPosition = vosWindow.scrollTop();
            vosWindow.scroll(function() {
                if (vosWindow.scrollTop() > navPosition) {
                    $('nav').removeClass('nav-down').addClass('nav-up');
                } else {
                    $('nav').removeClass('nav-up').addClass('nav-down');
                }
                navPosition = vosWindow.scrollTop();
            });
            navSmall();
        } else {
            navSmall();
        }
        $('.scroll-top').on('click', function() {
            $('html, body').stop().animate({ scrollTop: 0 }, 2000, 'easeInOutExpo');
            return false;
        });

        function elementsAnchor() {
            var hash = window.location.hash;
            if (hash != '') {
                setTimeout(function() {
                    $('html, body').stop().animate({
                        scrollTop: $(hash).offset().top - 59
                    }, 1000, 'easeInOutExpo');
                    history.pushState('', document.title, window.location.pathname);
                }, 500);
            }
        }
        elementsAnchor();
    }

    function bootstrapTools() {
        $('#accordion,#accordion2').on('show.bs.collapse', function() {
            $('#accordion .in').collapse('hide');
        });
        $("[data-toggle='tooltip']").tooltip();
        $('#buttonTabs a,#iconTabs a').click(function(e) {
            e.preventDefault();
            $(this).tab('show');
        });
    }

    function twitterFeedSliderInit() {
        if ($('#twitter-feed-slider').length) {
            $('#twitter-feed-slider ul').addClass('twitter-feed-slider navigation-thin');
            var twitterAutoSpeed = $('#twitter-feed-slider').attr('data-slider-speed');
            $('.twitter-feed-slider').owlCarousel({
                autoplay: true,
                autoplayTimeout: twitterAutoSpeed,
                items: 1,
                dots: false,
                mouseDrag: true,
                touchDrag: true,
                loop: true
            });
        }
    }

    $(document).ready(function() {
        $.when(heroContentSlider()).then(heroContentSliderFade());
        heroSliderOwl();
        progressBars();
        teamSlider();
        vossenIframes();
        parallaxVossen();
        clientsSlider();
        vosMap();
        sliderOwl();
        vossenHeader();
        bootstrapTools();
    });

    $(window).load(function() {
        twitterFeedSliderInit();
    });

    $(window).on('scroll', function() {

    });

}(jQuery));