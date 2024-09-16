function updateVisitCount() {
    let visit_counter_api = 'https://backend-cloudresume.azurewebsites.net/api'
    $.ajax({
        url: `${visit_counter_api}/visits`,
        method: 'GET',
        success: function(data) {
            console.log(data)
            $('#count').text(`${data.count}`);
            
            // Optionally increment the visit count
            $.ajax({
                url: `${visit_counter_api}/increment`,
                method: 'POST',
                success: function() {
                    // Optionally update the visit count again after increment
                    $.ajax({
                        url: `${visit_counter_api}/visits`,
                        method: 'GET',
                        success: function(data) {
                            $('#count').text(`${data.count}`);
                        },
                        error: function() {
                            console.error('Error fetching updated visit count.');
                        }
                    });
                },
                error: function() {
                    console.error('Error incrementing visit count.');
                }
            });
        },
        error: function() {
            console.error('Error fetching visit count.');
        }
    });
}

function setActiveNav() {
    $(".navbar-nav  .nav-link").on("click", function() {
        $(".navbar-nav").find(".active").removeClass("active");
        $(this).addClass("active");
    });
}
 
function toggleVcount() {
    if ($('#navbarSupportedContent').is(':visible')) {
      $('#visit-count').css('display', 'block');
    } else {
      $('#visit-count').attr('style', 'display: none !important;');
    }
}

function loadLanguage(lang) {
    $.getJSON(`javascript/languages/${lang}.json`, function (data) {
        // Iterate over each key-value pair in the JSON data
        $.each(data, function (key, value) {
            // Check if the key corresponds to an element's ID or class
            let $element = $('#' + key);
            if ($element.length) {
                // Replace text nodes within the element
                $element.html(value);
            }
        });
        var wordsToBold = [
            'Python', 'Pandas', 'SQL', 'SOLID', 'PEP8', 'FHIR','OMOP-CDM', 'HTML',
            'Javascript', 'CSS', 'Machine Learning'
        ];

        boldWords('experience', wordsToBold);
    });
}

function boldWords(divId, words) {
    var $div = $('#' + divId);
    var html = $div.html();
    words.forEach(function(word) {
        html = html.replaceAll(word, '<b>'+word+'</b>');
    });
    $div.html(html);

}


$(document).ready(function() {
    var $list = $('#technologies-list');  // Select the list
    var $listItems = $list.children('li');    // Get all list items

    // Sort the list items alphabetically based on the text inside the <div> tag
    $listItems.sort(function(a, b) {
        return $(a).find('div').text().toUpperCase().localeCompare($(b).find('div').text().toUpperCase());
    });

    // Append the sorted list items back to the list
    $list.append($listItems);

    updateVisitCount();
    setActiveNav();
    $(window).on('resize', toggleVcount);

    $("body").scrollspy({
        target: "#sideNav",
    });

    let currentLang = 'en';

    // Load the default language when the page loads
    loadLanguage(currentLang);
    $('input[type="radio"]').change(function () {
        if (this.id === 'english-option') {
            currentLang = 'en';
        } else if (this.id === 'french-option') {
            currentLang = 'fr';
        }
        loadLanguage(currentLang);
    });

    
});

