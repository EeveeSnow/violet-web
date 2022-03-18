const svg1 = document.getElementById("clouds_and_sun")
if (localStorage.getItem("colorTheme") == null){
    if (matchMedia("(prefers-color-scheme: dark)").matches == true) {
        var now_theme = "light"
    }
    else{
        var now_theme = "dark"
    }

}
else{
    var now_theme = localStorage.getItem("colorTheme")
}
changeScheme()

svg1.onclick = (e) => {
    changeScheme()
}

function changeScheme() {
    if (now_theme == "dark"){
        document.documentElement.style.cssText = `
        --main_color: lightgoldenrodyellow;
        --cloud_color: whitesmoke;
        --second_color: midnightblue;
        --sun_color: lightgoldenrodyellow;
        --sun_color__active: #F7FB3C;
        --sky_color: cornflowerblue;
        `
        document.querySelector('.sun__about').textContent = 'Ckick on Sun and Moon will rise';
        old_theme = now_theme
        now_theme = "light"
    }
    else{
        document.documentElement.style.cssText = `
        --main_color: midnightblue;
        --cloud_color: #707070;
        --second_color: #b3b3cd;
        --sun_color: #b3b3cd;
        --sun_color__active: whitesmoke;
        --sky_color: midnightblue;
        `
        document.querySelector('.sun__about').textContent = 'Ckick on Moon and Sun will rise';
        old_theme = now_theme
        now_theme = "dark" 
    }
    localStorage.setItem('colorTheme', old_theme);
}
    