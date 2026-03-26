const thumbnails = document.querySelectorAll(".thumb");
const lightbox = document.getElementById("lightbox");
const lightboxImg = document.getElementById("lightboxImg");
const closeBtn = document.getElementById("close");

// Open lightbox
thumbnails.forEach((img) => {
    img.addEventListener("click", () => {
        lightboxImg.src=img.src; //set clicked image
        lightbox.classList.add("show");
    })
})

//close button
closeBtn.addEventListener("click", () => {
    lightbox.classList.remove("show");
})

// close when clicking outside image
lightbox.addEventListener("click", (e) => {
    if (e.target === lightbox) {
        lightbox.classList.remove("show");
    }
})

