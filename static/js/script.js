let buttons = document.querySelectorAll(".bn");
let filter = document.querySelector(".filterWrapper");
let filterSidebar = document.querySelector(".filterSidebar");
let aboveBlur = document.querySelector(".aboveBlur");
let filterPic = document.getElementById("filterPic");

buttons.forEach(button => {
    button.addEventListener("click", function () {

        buttons.forEach(btn => {
            btn.classList.remove("active");
        });

        this.classList.add("active");
    });
});

filterSidebar.style.display = "none"
aboveBlur.style.display = "none"

filter.addEventListener("click", () => {
    filterSidebar.style.display == "none"
        ? (
            filterSidebar.style.display = "block",
            aboveBlur.style.display = "block",
            filterPic.src = "static/images/close.png"
        ) : (
            filterSidebar.style.display = "none",
            aboveBlur.style.display = "none",
            filterPic.src = "static/images/settings-sliders.png"
        )
})