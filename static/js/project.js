document.addEventListener("DOMContentLoaded", function() {
    const top_img = document.querySelector(".top_img img");
    const sub_imgs = document.querySelectorAll(".sub_img img");

    sub_imgs.forEach(function(sub_img) {
        sub_img.addEventListener("click", function() {
            top_img.src = sub_img.src;
        })
    })
})