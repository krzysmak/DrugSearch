const searchForm = document.getElementById("searchForm");

function handleSubmit(postForm) {
    searchForm.addEventListener("submit", e => {
        console.log("searchForm.val")
    })
}

handleSubmit(searchForm)