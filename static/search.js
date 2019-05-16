$("#search").keyup(function(){
    let data = {name: $(this)[0].value}
    $.ajax({
        url: "/search",
        method: "POST",
        data: data
    })
    .done(function(response){
        $("#users").html(response);
    })
})

$("#username").keyup(function(){
    let data = {username: $(this)[0].value}
    $.ajax({
        url: "/username",
        method: "POST",
        data: data
    })
    .done(function(response){
        $("#avail").html(response);
    })
})