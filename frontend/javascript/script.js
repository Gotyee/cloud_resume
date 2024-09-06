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
                            $('#visit-count').text(`Visit Count: ${data.count}`);
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

    $("body").scrollspy({
        target: "#sideNav",
    });
});

