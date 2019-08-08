var numberOfImages = document.querySelectorAll(".countImage");
var numberOfBrand = document.querySelectorAll(".countBrand");
var numberOfPrice = document.querySelectorAll(".countPrice");
var numberOfPresentage = document.querySelectorAll(".countPresentage");
var numberOfFeature1 = document.querySelectorAll(".countFeature1");
var numberOfFeature2= document.querySelectorAll(".countFeature2");

/*
var data={
        "pids":['1','2','3','4','5','6','7'],
        table_data: [
            ['PRODUCT', 'img1','img2','img3','img4','img5','img6','img7'],
            ['IMAGE', 'img1','img2','img3','img4','img5','img6','img7'],
            ['BRAND','brand1','brand2','brand3','brand4','brand5','brand6','brand7'],
            ['PRICE', 9999, 9999, 9999, 9999, 9999, 9999, 9999],
            ['VOTES', 0.3, 0.75, 0.45, 0.15, 0.98, 0.0, 1.0],
            ['FEATURE 1', 'val1', 'val1', 'val1', 'val1', 'val1', 'val1', 'val1'],
            ['FEATURE 2', 'val2', 'val2', 'val2', 'val2', 'val2', 'val2', 'val2']
        ]
};
*/

$(document).ready(function(){
    $.ajax({
        type: 'POST',
        url: 'compare_products',
        success: function(data){
            setValue(JSON.parse(data));
        }
    });
});

    


function setValue(data){
    
    // We make the html for the table
    var table_html_str = "";
    table_html_str += "<table>";
    for (var i=0; i<data['table_data'].length; i++){
        table_html_str += "<tr>";
        for (var j=0; j<data['table_data'][0].length; j++){
            var cell_tag = 'th';
            if (i !== 0 && j !== 0){
                cell_tag = 'td'
            }
            table_html_str += '<' + cell_tag + '>';
            if (j === 0){
                table_html_str += data['table_data'][i][j];
            } else {
                if(i === 0){
                    table_html_str += '<button class="product">';
                    table_html_str += data['table_data'][i][j];
                    table_html_str += '</button>';
                } else if(i === 1){
                    table_html_str += '<img class="img-responsive" src="/static/images/'+ data['table_data'][i][j] +'">';
                } else if(i === 3){
                    table_html_str += '$' + data['table_data'][i][j];
                } else if( i === 4){
                     table_html_str +=((data['table_data'][i][j])*100) + '%'
                }
                else {
                    table_html_str += data['table_data'][i][j];
                }
            }
            table_html_str += '</' + cell_tag + '>';
        }
        table_html_str += "</tr>";
    } 
    table_html_str += "</table>";
    table_div = document.querySelector('div.table');
    table_div.innerHTML = table_html_str;

    var product = document.querySelectorAll(".product");
    for (var i=0;i<data['pids'].length;i++){
        product[i].id=data['pids'][i];
        const pid = product[i].id;
         product[i].addEventListener("click",function(){
            window.location.href = 'product?pid='+ pid;
        });
    }
}
