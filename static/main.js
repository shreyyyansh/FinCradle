fetch("/category-leak")
.then(r=>r.json())
.then(d=>{
    document.getElementById("leak").innerText = d.leak;
});
