$(document).ready(function(){
    var themeDefault = 'light';

    if ($("body").hasClass("dark")) {
        themeDefault = 'dark';
    }

    var setNight = localStorage.getItem("night");
    var setDay = localStorage.getItem("day");


    var DarkModeText = $(".mode-checkbox-label").attr("data-dark-title"),
        LightModeText = $(".mode-checkbox-label").attr("data-light-title");

    if (themeDefault == 'light') {

        if (setNight) {
            $("body").addClass("dark");
            $("body").addClass("dark-loaded");
            $(".mode-checkbox-label").text(LightModeText);
            $("#mode-checkbox").prop("checked", true);
        } else {
            $(".mode-checkbox-label").text(DarkModeText);
        }

        $("#mode-checkbox").on("change", function(){
            var setNight = localStorage.getItem("night");

            if ($(this).is(':checked')) {
                $("body").addClass("dark");
                localStorage.setItem("night",1);
            } else {
                $("body").removeClass("dark");
                localStorage.removeItem("night");
            }
        });
    }

    if (themeDefault == 'dark') {

        if (setDay) {
            $("body").removeClass("dark");
            $("body").removeClass("dark-loaded");
            $("#mode-checkbox").removeAttr("checked");
            $(".mode-checkbox-label").text(DarkModeText);

        } else {
            $(".mode-checkbox-label").text(LightModeText);
        }

        $("#mode-checkbox").on("change", function(){
            var setDay = localStorage.getItem("day");

            if ($(this).is(':checked')) {
                $("body").addClass("dark");
                localStorage.removeItem("day");
            } else {
                $("body").removeClass("dark");
                localStorage.setItem("day", 1);
            }
        });
    }

    setTimeout(function(){
        $(".mode-check label").addClass("transition");
    }, 100);

})