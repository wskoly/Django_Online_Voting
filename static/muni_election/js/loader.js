$(window).on('load', function () {
    console.log("loading....");
    setTimeout(removeLoader, 10); //wait for page load PLUS 10 miliseconds.
});
function removeLoader() {
    $("#loader").fadeOut(500, function () {
        var koly = document.getElementById("loader");
        koly.remove(); //makes page more lightweight 
        console.log("loading finished");
    });
}