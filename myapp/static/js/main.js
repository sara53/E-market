var categoriesList = document.querySelector("div.displayMenu");
var BrandList = document.querySelector("div.displayMenu2");
var selectForComparison = document.querySelectorAll(".box-price input");
var numberOfSelected=document.querySelector('span.number');
var count=0;
var btnNav = document.querySelector('button.nav-button');
var product = document.querySelectorAll(".box-price");
var viewDetails = document.querySelectorAll('div.Order-now p');
var nameOfProduct = document.querySelectorAll('div.box-price h2.text-primary');
var nameOfCompany = document.querySelectorAll('div.box-price span.companyName');
var priceOfProduct = document.querySelectorAll('div.price-order div.price p');
var imageProduct = document.querySelectorAll('div.box-price div.center-block img');
var percentOfproduct =document.querySelectorAll('div.box-price div.likes span.innerPresent');


$(document).ready(function (){
    
    var scrollTop = $(".scroll-top");
    $(window).scroll(function(){
        if($(this).scrollTop() >= 300){
            scrollTop.show();
        }
        else{
            scrollTop.hide();
        }
    });
    
    scrollTop.click(function(){
        $("html,body").animate({scrollTop : 0}, 600);
    });
    
    // post request categories
    $.ajax({
        type: 'POST',
        url: 'get_categories',
        success: function(data){
            populate_categories(JSON.parse(data));
        }
    });
    // post request brand
    $.ajax({
        type: 'POST',
        url: 'get_brands',
        success: function(data){
            populate_brands(JSON.parse(data));
        }
    });

    // populate products
    view_all_products();
    
    //open subMenu
    $(".openMenu").click(function(){
        $(".displayMenu").slideToggle(1000);
    });
    $(".openMenu2").click(function(){
        $(".displayMenu2").slideToggle(1000);
    });
    
    // get request compare n products
    btnNav.addEventListener("click",function(){    
        var str = "compare?count="+numberOfSelected.innerHTML;
        var count=0;
        checkBoxes = document.querySelectorAll('input.select-for-comp');
        for(let i=0; i<checkBoxes.length; i++){
            if(checkBoxes[i].checked===true){
                id=checkBoxes[i].parentElement.id;
                count++;
                str += "&pid"+count+"="+id;
            }
        }
        window.location.href = str;
    });
    
    // btn view details
    for(let i=0; i<viewDetails.length; i++){
        viewDetails[i].addEventListener("click",function(){
            window.location.href = 'product?pid='+ selectForComparison[i].parentElement.id;
        });
    }
    
    // post request view_all_products
    $('input.productName').on("keyup",function(){
        view_all_products();
    });
    $('.fromInput').on("keyup",function(){
        view_all_products();
    });
    $('.toInput').on("keyup",function(){
        view_all_products();
    });
    $('.fromInput').on("change",function(){
        view_all_products();
    });
    $('.toInput').on("change",function(){
        view_all_products();
    });
    
});

function viewDetailsClicked(viewDetailsDiv){
    window.location.href = 'product?pid=' + viewDetailsDiv.parentElement.parentElement.id;
}

function fillProduct(data){
    productsContainer = document.querySelector('#products-container');
    productsContainer.innerHTML = '';
    for(let i=0; i<data.length; i++){
        var str = '';
        var votes_bar_width_percentage = (Math.round(data[i].pos_percentage*100)) + '%';
        str += '<div class="col-md-4 col-sm-6">';
            str += '<div class="box-price" id="'+data[i].pid+'">';
                str += '<h2 class="text-primary">'+data[i].pname+'</h2>';
                str += '<span class="companyName">'+data[i].brand+'</span>';
                str += '<div class="center-block img-responsive">';
                    str += '<img class="center-block" src="/static/images/'+data[i].img+'">';
                str += '</div>';
                str += '<input class="select-for-comp" type="checkbox" onclick="selectForComparisonCheckboxClicked(this)"> <span class="checkspan">choose for comparsion</span>';
                str += '<div class="likes">';
                    str += '<i class="fa fa-thumbs-up fa-lg"></i>';
                    str += '<span class="likePresent">';
                        str += '<span class="innerPresent" style="width: '+votes_bar_width_percentage+';">'+votes_bar_width_percentage+'</span>';
                    str += '</span>';
                    str += '<i class="fa fa-thumbs-down fa-lg"></i>';
                str += '</div>';
                str += '<div class="price-order">';
                    str += '<div class="price">$'+data[i].price+'</div>';
                    str += '<div class="Order-now clickable" onclick="viewDetailsClicked(this)">View Details</div>';
                str += '</div>';
            str += '</div>';
        str += '</div>';

        productsContainer.innerHTML += str;
    }

}

function selectForComparisonCheckboxClicked(cbox){
    btnNav.disabled = false;
    if(cbox.checked===true){
        count++;
        numberOfSelected.innerHTML = count;
    }else if(cbox.checked===false){
        count--;
        if(count===0){
            btnNav.disabled = true;
        }
        numberOfSelected.innerHTML = count;
    }
}

function populate_brands(data){
    BrandList.innerHTML="";
    for(let i=0; i<data.length; i++){
        var node = document.createElement("p");
        var node2 = document.createElement("input");
        var textnode = document.createTextNode(data[i]);
        node2.type='checkbox';
        node.appendChild(textnode);
        BrandList.appendChild(node2);
        BrandList.appendChild(node);
        $('.Subcategory .displayMenu2 input').on("click",function(){
            view_all_products();
        });
    }
}

function populate_categories(data){
    categoriesList.innerHTML="";
    for(let i=0; i<data.length; i++){
        var node = document.createElement("p");
        var node2 = document.createElement("input");
        var textnode = document.createTextNode(data[i]);
        node2.type='checkbox';
        node.appendChild(textnode);
        categoriesList.appendChild(node2);
        categoriesList.appendChild(node);
        $('.Subcategory .displayMenu input').on("click",function(){
            view_all_products();
        });
    }
}

function send_view_all_products_request(params_object){
    $.ajax({
        type: 'POST',
        url: 'view_all_products',
        data: params_object,
        success: function(data){
            fillProduct(JSON.parse(data));
        }
    });
}

function view_all_products(){

    count = 0;
    btnNav.disabled = true;
    numberOfSelected.innerHTML = count;

    var name,
        from,
        to,
        noCategories,
        noBrands,
        allCheckedCategories,
        allCheckedBrands;
    var params_accumulator = {};

    // input name of product
    if($('.productName').val()===""){
       name = "****";
    }else{
        name = $('.productName').val();
    }
    params_accumulator['name'] = name;

    // minimum input
    if($('.fromInput').val()===""){
        from = 0;
    }else{
        var p = Math.round(parseFloat($('.fromInput').val()));
        if (p < 0){
            $('.fromInput').val(0);
            p = 0;
        }
        from = p;
    }
    params_accumulator['price_min'] = from;

    // maximum input
    if($('.toInput').val()===""){
        to = 0;
    }else{
        var p = Math.round(parseFloat($('.toInput').val()));
        if (p < 0){
            $('.toInput').val(0);
            p = 0;
        }
        to = p;
    }
    params_accumulator['price_max'] = to;

    // number of categories and name
    allCheckedCategories = $('.Subcategory .displayMenu :checkbox:checked').next();
    noCategories = allCheckedCategories.length;
    params_accumulator['num_of_categories'] = noCategories;
    for(var i=0; i<noCategories; i++){
        params_accumulator['category'+(i+1)] = allCheckedCategories[i].innerHTML;
    }
    // number of brands and name of categories
    allCheckedBrands = $('.Subcategory .displayMenu2 :checkbox:checked').next();
    noBrands = allCheckedBrands.length;
    params_accumulator['num_of_brands'] = noBrands;
    for(var j=0; j<noBrands; j++){
        params_accumulator['brand'+(j+1)] = allCheckedBrands[j].innerHTML;
    }

    send_view_all_products_request(params_accumulator);
}


