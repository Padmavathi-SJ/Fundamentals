const content = document.getElementById("content");
const loading = document.getElementById("loading");

let page = 1;
let isLoading = false;

//simulate API 
async function fetchData(page) {
    const res = await fetch(`https://jsonplaceholder.typicode.com/posts?_limit=5&_page=${page}`);
    const data = await res.json();
    return data.map(item => item.title);
}

//Load content
async function loadMore() {
    if (isLoading) return;

    isLoading = true;
    loading.style.display = "block";

    const data = await fetchData(page);

    //stop if no more data
    if(data.length === 0) {
        loading.textContent = "No more data";
        return;
    }

    data.forEach(item => {
        const div = document.createElement("div");
        div.classList.add("card");
        div.textContent = item;
        content.appendChild(div);
    });

    page++;
    isLoading = false;
    loading.style.display = "none";

}

// Detect scroll
window.addEventListener("scroll", () => {
    if (isLoading) return;
    
    const scrollTop = window.scrollY;
    const windowHeight = window.innerHeight;
    const fullHeight = document.body.scrollHeight;

    // If near bottom
    if(scrollTop + windowHeight >= fullHeight - 50) {
        loadMore();
    }
});

//Initial load
loadMore();