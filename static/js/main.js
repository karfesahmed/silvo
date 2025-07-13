document.addEventListener("DOMContentLoaded",()=>{
    products_list();

})

function products_list(){
    const products = document.querySelector(".products");
    fetch("http://localhost:8000/products/").then(res=>res.json())
    .then((data)=>{
        products.innerHTML += "";
        data.forEach((product)=>{
            
            products.innerHTML += `
            
                <div class="col-12 col-sm-6 col-md-4 col-lg-3 mb-4 mx-auto product" id="${product.id}">
                <a href="/product/${product.id}">
                    <div class="card h-100 shadow-sm mycard">
                        
                        <img src="${product.imgs[0]?.image || 'static/images/placeholder.png'}" class="card-img-top" alt="placeholder" style="width: 100%; height: 200px; object-fit: cover;">
                        <div class="card-body d-flex flex-column">
                            <h4>${truncateText( product.name, 20)}</h4>
                            <p class="card-text mb-3">
                                ${truncateText(product.description, 100) }
                            </p>
                            <div class="mt-auto">
                                
                                <div class="d-flex justify-content-between align-items-center">
                                    <span class="fw-bold text-success">${product.price} DA</span>
                                </div>

                            </div>
                        </div>
                        
                    </div>
                </a>
                </div>
            
            `;

        })
        
    })
}
function truncateText(text, maxLength) {
    if (text.length > maxLength) {
        return text.slice(0, maxLength) + "...";
    }
    return text;
}
