document.getElementById("demo").innerHTML = "Hello World!";
console.log("Connected!");
var btn = document.getElementById("btn");
var first=true;
btn.addEventListener("click", onClick0);
var xhr = new XMLHttpRequest();
var object = {"Id": 78912, "Customer": "Jason Sweet", "Quantity": 0, "Price": 18.00, "Total": 0.00};
function onClick0(){
    xhr.open("POST", "192.168.0.120");
    xhr.setRequestHeader("Accept", "application/json");
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            console.log(xhr.status);
            let obj=JSON.parse(xhr.responseText)
            console.log(obj);
            if(first){
                first=false;
                btn.innerHTML="Increment!"
                for (const el in obj){
                    if (el!=="Success"){
                        var div = document.createElement('div');  //creating element
                        div.textContent = el+": "+obj[el];         //adding text on the element
                        document.getElementById("div0").appendChild(div);
                    }
                }
            } else{
                const div0 = document.getElementById("div0");
                const divs=Array.from(div0.children);
                var i=0;
                for (const el in obj){
                    if (el!=="Success"){
                        divs[i].textContent = el+": "+obj[el]; 
                        i++;
                    }
                }
            }
    }};
    object.Quantity++;
    object.Total+=object.Price;
    data=JSON.stringify(object);
    xhr.send(data);
    
}