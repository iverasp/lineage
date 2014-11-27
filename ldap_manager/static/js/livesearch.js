$(document).ready(function(){
    $("#query").autocomplete({
        source: [],
        select: function( event, ui ) {
            event.preventDefault();
            $("#query").val(ui.item.label);
            window.location.href = ui.item.value;
        },
        focus: function( event, ui ) {
            $("#query").val(ui.item.label);
        },
        minLength: 3,
        delay: 500,
    });

    $("input#query").keyup(function(){
        var query = $(this).val();

        if(query.length>3){
            dataString = 'q=' + query;
            $.ajax({
                type: "POST",
                url: "/api/v1/ajaxsearch/",
                data: dataString,
                success: function(response){
                  console.log(response)
                    var availableHints = [];
                    for (var i in response.users){
                        availableHints.push({
                            value: "/user/" + response.users[i].username,
                            label: response.users[i].full_name
                        });
                    }
                    $("#query").autocomplete({
                        source: availableHints,
                    });
                }
            });
        }
    });
});
