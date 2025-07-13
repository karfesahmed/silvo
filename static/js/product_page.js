document.addEventListener("DOMContentLoaded",()=>{
    
    const name = document.querySelector("#name").innerHTML;
    document.querySelector("#name").innerHTML = truncateText(name,16);
    if(document.querySelector("#other")!==null){
        other();
    }

    get_wilayas();
    get_shipping();
    document.querySelector("#quantity").addEventListener("change",(e)=>{
        const currunt_price = parseInt(document.querySelector("#product-price").innerHTML);
        const currunt_quantity = parseInt(e.target.value);
        let shipping = document.querySelector("#select_wilaya").value
        const shipping_amount = parseInt(shipping.split(",")[1])

        const count_badge = document.querySelector("#count");
        count_badge.innerHTML = `${currunt_quantity}&times;`;

        const total_price = document.querySelector("#total");
        if(shipping === ""){
            total_price.innerHTML = `${currunt_price} د.ج`;
        }else{
            total_price.innerHTML = `${currunt_price*currunt_quantity + shipping_amount} د.ج`;
        }
        
        
        
    })
    quantity();
    
});


function quantity(){
    const btn_increase = document.querySelector("#increase");
    const btn_decrease = document.querySelector("#decrease");
    const inp = document.querySelector("#quantity");
    
    console.log(shipping)
    
        btn_increase.addEventListener("click",()=>{
            if(document.querySelector("#select_wilaya").value === ""){
                alert("اختر ولايتك")
            }else{
                let counter = parseInt(inp.value);
                counter++;
                inp.value = counter;
                inp.dispatchEvent(new Event("change"))
            }
        })
        btn_decrease.addEventListener("click",()=>{
            if(document.querySelector("#select_wilaya").value === ""){
                alert("اختر ولايتك")
            }else{
                let counter = parseInt(inp.value);
                if(counter > 1){   
                    counter--;
                    inp.value = counter;            
                    inp.dispatchEvent(new Event("change"));
                }
            }
        })
    

}

function other(){
    document.querySelector("#other").addEventListener("change",()=>{
        
        const size_or_color = document.querySelector("#other").value;
        
        if(size_or_color !== ""){
            let test = size_or_color.split(",");
            if(test.length === 2){
                let price = parseInt(test[1]);
                document.querySelector("#product-price").innerHTML = price;
                document.querySelector("#price-quan").innerHTML = `${price} د.ج`;
                const input = document.querySelector("#quantity");
                input.value = 1;
                input.dispatchEvent(new Event("change"))
                console.log(price);
            }
        }
    });
    
    
}

function get_wilayas(){
    const select_wilaya = document.querySelector("#select_wilaya");
    fetch("http://localhost:8000/wilayas").then(res=>res.json())
    .then((data)=>{
        data.forEach((wilaya)=>{
            select_wilaya.innerHTML += `
                <option value="${wilaya.IDWilaya},${wilaya.delivery_home},${wilaya.delivery_office}">${wilaya.IDWilaya}- ${wilaya.name}</option>
            `;
        })
    })
}

function get_shipping(){
    document.querySelector("#select_wilaya").addEventListener("change",(e)=>{
        const shipping = parseInt(e.target.value.split(",")[1]);
        const currunt_price = parseInt(document.querySelector("#product-price").innerHTML);
        document.querySelector("#shipping").innerHTML = `${shipping} د.ج`;
        document.querySelector("#total").innerHTML = `${parseInt(currunt_price)+shipping} د.ج`;
    })
}


function truncateText(text, maxLength) {
    if (text.length > maxLength) {
        return text.slice(0, maxLength) + "..";
    }
    console.log(text);
    
    return text;
}


