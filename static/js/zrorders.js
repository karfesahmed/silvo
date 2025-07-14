document.addEventListener("DOMContentLoaded",()=>{
    get_orders()
})


function get_orders() {
    const orders_page = document.querySelector("#orders");
    orders_page.innerHTML = "<p>جاري تحميل الطلبات...</p>";
    
    fetch("https://silvo.onrender.com/wilayas")
        .then(res => res.json())
        .then((wilayas) => {
            const wilayaMap = {};
            wilayas.forEach(w => {
                wilayaMap[w.id] = w.name;
            });

            
            fetch("https://silvo.onrender.com/zr/orders")
                .then(res => res.json())
                .then((data) => {
                    orders_page.innerHTML = '';

                    const d = data.Colis;
                    d.forEach((order) => {
                        const wilayaName = wilayaMap[order.IDWilaya] || "غير معروفة";

                        all_orders(
                            order.id_Externe,
                            order.Client,
                            order.MobileA,
                            wilayaName,
                            order.Adresse,
                            order.TProduit,
                            order.Total,
                            order.Note,
                            orders_page,
                            order.TypeLivraison,
                            order.Situation
                        );
                    });
                })
                .catch(err => {
                    console.error("فشل تحميل الطلبات", err);
                    orders_page.innerHTML = "<p>حدث خطأ أثناء تحميل الطلبات.</p>";
                });
        })
        .catch(err => {
            console.error("فشل تحميل الولايات", err);
            orders_page.innerHTML = "<p>حدث خطأ أثناء تحميل الولايات.</p>";
        });
}



function all_orders(id,Client,MobileA,wilaya,Adresse,TProduit,Total,note,page,TypeLivraison,Situation){
    let typeL = "المنزل"
    if(TypeLivraison===1){
        typeL = "المكتب"
    }
    page.innerHTML += `
    
                        <div class="d-flex align-items-center border rounded shadow-sm mb-2 px-2 py-2 card-order" style="min-width: 1400px; font-size: 0.8rem;">
                            <div style="width: 60px;" class="text-center">#${id}</div>
                            
                            <div style="width: 120px;" class="text-center">${Client}</div>
                            <div style="width: 130px;" class="text-center">${MobileA}</div>
                            <div style="width: 100px;" class="text-center">${wilaya}</div>
                            <div style="width: 200px;" class="text-center">${truncateText(Adresse,25) }</div>

                            
                            
                                <div style="width: 110px;" class="text-center">
                                    ${typeL}
                                </div>

                                <!-- ملاحظة -->
                                <div style="width: 200px;" class="text-center">
                                    ${truncateText(note,30)}
                                </div>

                                <!-- الحالة -->
                                <div style="width: 250px;" class="text-center">
                                    <mark>${Situation}</mark>
                                </div>

                                <!-- المنتج والكمية والسعر -->
                                <div style="width: 150px;" class="text-center">${truncateText(TProduit,18) }</div>
                                
                                <div style="width: 100px;" class="text-center">
                                    ${Total} DA
                                </div>
                        </div>
                    `;
}


function truncateText(text, maxLength) {
    if (text.length > maxLength) {
        return text.slice(0, maxLength) + "..";
    }
    console.log(text);
    
    return text;
}
