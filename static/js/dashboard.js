document.addEventListener("DOMContentLoaded",()=>{
    get_orders()
})


function get_orders(){
    const orders_page = document.querySelector("#orders")
    fetch("http://localhost:8000/orders").then(res=>res.json())
    .then((data)=>{
        orders_page.innerHTML='';
        data.forEach((order)=>{
                if(order.Confrimee !== "1"){
                    fetch(`http://localhost:8000/wilayas/${order.IDWilaya}`).then(re=>re.json())
                    .then((wilaya)=>{
                        if(order.conferme === "0"){
                            all_orders(order.id,order.Client,order.MobileA,wilaya.name,order.Adresse,order.TProduit,order.quantity,order.Total,order.Note,orders_page);
                        }
                        
                        document.querySelectorAll(".status-filter").forEach((btn)=>{
                            btn.addEventListener("click",(e)=>{
                                orders_page.innerHTML = '';
                                if(e.target.id === "all"){
                                    if(order.conferme === "0"){
                                        all_orders(order.id,order.Client,order.MobileA,wilaya.name,order.Adresse,order.TProduit,order.quantity,order.Total,order.Note,orders_page);
                                    }
                                }else if(e.target.id === "confirm"){
                                    if(order.conferme === "1"){
                                        all_orders(order.id,order.Client,order.MobileA,wilaya.name,order.Adresse,order.TProduit,order.quantity,order.Total,order.Note,orders_page);
                                    }
                                }else if(e.target.id === "delay"){
                                    if(order.conferme === "2"){
                                        all_orders(order.id,order.Client,order.MobileA,wilaya.name,order.Adresse,order.TProduit,order.quantity,order.Total,order.Note,orders_page);
                                    }
                                }else if(e.target.id === "no_answer"){
                                    if(order.conferme === "3"){
                                        all_orders(order.id,order.Client,order.MobileA,wilaya.name,order.Adresse,order.TProduit,order.quantity,order.Total,order.Note,orders_page);
                                    }
                                }
                                else if(e.target.id === "cancel"){
                                    if(order.conferme === "4"){
                                        all_orders(order.id,order.Client,order.MobileA,wilaya.name,order.Adresse,order.TProduit,order.quantity,order.Total,order.Note,orders_page);
                                    }
                                }
                                
                            })
                        })
                    })
            }
        })
    })
}



function all_orders(id,Client,MobileA,wilaya,Adresse,TProduit,quantity,Total,note,page){
    const csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    page.innerHTML += `
    <form method="post">
    <input type="hidden" name="csrfmiddlewaretoken" value="${csrf_token}">
                        <div class="d-flex align-items-center border rounded shadow-sm mb-2 px-2 py-2 card-order" style="min-width: 1400px; font-size: 0.8rem;">
                            <div style="width: 60px;">#${id}</div>
                            <input type="hidden" name="order_id" value="${id}">
                            <div style="width: 120px;">${Client}</div>
                            <div style="width: 130px;">${MobileA}</div>
                            <div style="width: 100px;">${wilaya}</div>
                            <div style="width: 200px;">${truncateText(Adresse,25) }</div>

                            
                            
                                <div style="width: 110px;">
                                    <select class="form-select form-select-sm" name="typeLivr">
                                        <option value="0" selected>المنزل</option>
                                        <option value="1">المكتب</option>
                                    </select>
                                </div>

                                <!-- ملاحظة -->
                                <div style="width: 180px;">
                                    <textarea name="note" class="form-control form-control-sm" rows="1" placeholder="...">${note}</textarea>
                                </div>

                                <!-- الحالة -->
                                <div style="width: 110px;">
                                    <select class="form-select form-select-sm" name="status">
                                        <option value="0">لم يراجع</option>
                                        <option value="1">تأكيد</option>
                                        <option value="2">تأجيل</option>
                                        <option value="3">لم يرد</option>
                                        <option value="4">إلغاء</option>
                                    </select>
                                </div>

                                <!-- المنتج والكمية والسعر -->
                                <div style="width: 150px;">${truncateText(TProduit,18) }</div>
                                <div style="width: 80px;">
                                    <input type="number" style="width: 60px;" name="new_quantity" value="${quantity}">
                                </div>
                                <div style="width: 100px;">
                                    <input type="text" style="width: 60px;" name="new_price" value="${Total}"> DA
                                </div>
                                

                                
                                <div style="width: 80px;">
                                    <button class="btn btn-sm btn-primary sub" name="sub" value="${id}" >✔تأكيد</button>
                                </div>
                                <div style="width: 150px;">
                                    <button class="btn btn-sm btn-primary sub" name="sub" value="send">ارسل لشركة التوصيل</button>
                                </div>
                            
                        </div>
    </form>                `;
}


function truncateText(text, maxLength) {
    if (text.length > maxLength) {
        return text.slice(0, maxLength) + "..";
    }
    console.log(text);
    
    return text;
}
