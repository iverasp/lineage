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
    })
    // show icon next to result
    .data( "ui-autocomplete" )._renderItem = function( ul, item ) {
      return $( "<li></li>" )
      .data( "item.autocomplete", item )
      .append( "<img width='16' height='16' src=" + item.icon + "/>  " + item.label)
      .appendTo( ul );
    };

    $("input#query").keyup(function(){
        var query = $(this).val();

        if(query.length>3){
            dataString = 'q=' + query;
            $.ajax({
                type: "POST",
                url: "/api/v1/ajaxsearch/",
                data: dataString,
                success: function(response){

                    var availableHints = [];
                    for (var i in response.users){
                        availableHints.push({
                            icon: '/static/img/user.svg',
                            value: "/user/" + response.users[i].username,
                            label: response.users[i].full_name
                        });
                    }
                    for (var i in response.groups){
                        availableHints.push({
                            icon: '/static/img/group.svg',
                            value: "/group/" + response.groups[i].name,
                            label: response.groups[i].name
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
