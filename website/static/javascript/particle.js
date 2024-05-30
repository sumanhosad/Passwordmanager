$.getScript("https://cdnjs.cloudflare.com/ajax/libs/particles.js/2.0.0/particles.min.js", function(){
    particlesJS('particles-js',
      {
        "particles": {
          "number": {
            "value": 100,
            "density": {
              "enable": true,
              "value_area": 500
            }
          },
          "color": {
            "value": "#ffffff"
          },
          "shape": {
            "type": "circle",
            "stroke": {
              "width": 0,
              "color": "#ffffff"
            },
            "polygon": {
              "nb_sides": 5
            },
            "image": {
              "width": 100,
              "height": 100
            }
          },
          "opacity": {
            "value": 0.5,
            "random": false,
            "anim": {
              "enable": false,
              "speed": 1,
              "opacity_min": 0.1,
              "sync": false
            }
          },
          "size": {
            "value": 3,
            "random": true,
            "anim": {
              "enable": false,
              "speed": 40,
              "size_min": 0.1,
              "sync": false
            }
          },
          "line_linked": {
            "enable": true,
            "distance": 150,
            "color": "#ffffff",
            "opacity": 0.4,
            "width": 1
          },
          "move": {
            "enable": true,
            "speed": 6,
            "direction": "none",
            "random": false,
            "straight": false,
            "out_mode": "out",
            "attract": {
              "enable": false,
              "rotateX": 600,
              "rotateY": 1200
            }
          }
        },
        "interactivity": {
          "detect_on": "canvas",
          "events": {
            "onhover": {
              "enable": true,
              "mode": "repulse"
            },
            "onclick": {
              "enable": true,
              "mode": "push"
            },
            "resize": true
          },
          "modes": {
            "grab": {
              "distance": 400,
              "line_linked": {
                "opacity": 1
              }
            },
            "bubble": {
              "distance": 400,
              "size": 40,
              "duration": 2,
              "opacity": 8,
              "speed": 3
            },
            "repulse": {
              "distance": 100
            },
            "push": {
              "particles_nb": 4
            },
            "remove": {
              "particles_nb": 2
            }
          }
        },
        "retina_detect": true,
        "config_demo": {
          "hide_card": false,
          "background_color": "#b61924",
          "background_image": "",
          "background_position": "50% 50%",
          "background_repeat": "no-repeat",
          "background_size": "cover"
        }
      }
    );

});
function goBack() {
            window.history.back();
        }

    // Get all buttons with class "copy-btn"
    var copyButtons = document.querySelectorAll('.copy-btn');

    // Loop through each button and add a click event listener
    copyButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            // Get the input field next to the clicked button
            var inputField = this.previousElementSibling;

            // Select the text in the input field
            inputField.select();

            // Copy the selected text to the clipboard
            document.execCommand('copy');
        });
    });


// Get all buttons with class "accordion"
var accordions = document.querySelectorAll('.accordion');

// Loop through each button and add a click event listener
accordions.forEach(function(accordion) {
    accordion.addEventListener('click', function() {
        // Close all other open panels
        accordions.forEach(function(otherAccordion) {
            if (otherAccordion !== accordion) {
                otherAccordion.classList.remove('active');
                var otherPanel = otherAccordion.nextElementSibling;
                otherPanel.style.maxHeight = null;
                otherPanel.classList.remove("show");
            }
        });

        // Toggle the class "active" to highlight the button
        this.classList.toggle('active');

        // Toggle the next sibling element (which is the panel)
        var panel = this.nextElementSibling;
        if (panel.style.maxHeight) {
            panel.style.maxHeight = null;
            panel.classList.remove("show");
        } else {
            panel.style.maxHeight = panel.scrollHeight + "px";
            panel.classList.add("show");
        }
    });
});

$(document).ready(function() {
        $('#search-query').on('input', function() {
            let query = $(this).val().toLowerCase();
            let found = false;
            $('.accordion').each(function() {
                let text = $(this).text().toLowerCase();
                let panel = $(this).next('.panel');
                let matches = false;

                // Check if the accordion button or any of its panel items match the query
                if (text.includes(query)) {
                    matches = true;
                } else {
                    panel.find('.password-item input').each(function() {
                        if ($(this).val().toLowerCase().includes(query)) {
                            matches = true;
                        }
                    });
                }

                if (matches) {
                    $(this).show();
                    panel.show();
                    found = true;
                } else {
                    $(this).hide();
                    panel.hide();
                }
            });

            // Show or hide the "no results" message
            if (!found) {
                $('#password-list').hide();
                $('#no-results').show();
            } else {
                $('#password-list').show();
                $('#no-results').hide();
            }
        });
    });

