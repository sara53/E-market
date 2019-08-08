var nameProducts = document.querySelector('div.priceBox h2.textPrimary');
var nameCompany = document.querySelector('div.priceBox span.companySpan');
var priceNum = document.querySelector('div.priceBox div.priceProduct');
var percentage = document.querySelector('div.likesIcons span.innerSpan');
var sliderImage = document.querySelector('div.carousel-inner');
var tableContent = document.querySelector('div.tableContent table');
var scrollCommentDiv = document.querySelector('div.scrollComment');
var textName,textComment;


function addCommentClicked(btn){


    event.preventDefault();
    textName = $('.name').val();
    if($('.name').val()===""){
        textName="ANONYMOUS";
    }
    const tName = textName;
    const textComment = $('.comment').val();
    if(textComment === ''){
        alert("Comment can't by empty!");
        return false;
    }

    $.ajax({
        type: 'POST',
        url: 'add_comment',
        data: ({"name":tName, "comment":textComment}),
        success: function(data)
        {
            var votes_bar_width_percentage = (Math.round(parseFloat(data)*100)) + '%';
            $('span.innerSpan').width(votes_bar_width_percentage);
            $('span.innerSpan').html(votes_bar_width_percentage);

            $.ajax({
                type: 'POST',
                url: 'view_comments',
                success: function(data)
                {
                    viewCommnts(JSON.parse(data));
                }
            });
        }
    });
    document.querySelector('textarea.comment').value = '';
    return false;
}


$(document).ready(function(){
    
    // view product info
    $.ajax({
        type: 'POST',
        url: 'view_product',
        success: function(data)
        {
            viewProduct(JSON.parse(data));
        }
    });
    
    // view product comments
    $.ajax({
        type: 'POST',
        url: 'view_comments',
        success: function(data)
        {
            viewCommnts(JSON.parse(data));
        }
    });
    
    // slider
    $(".carousel").carousel({
        interval: 4000
    });
});

function viewProduct(data){

    nameProducts.innerHTML = data.pname;
    nameCompany.innerHTML = data.brand;
    priceNum.innerHTML = '$'+data.price;
    var votes_bar_width_percentage = (Math.round(data.pos_percentage*100)) + '%';
    $('span.innerSpan').width(votes_bar_width_percentage);
    $('span.innerSpan').html(votes_bar_width_percentage);
    sliderImage.innerHTML = "";
    for(var i=0; i<data.images.length; i++){
        var imagesItem = document.createElement('div');
        var nodes = document.createElement('img');
        imagesItem.className = "item";
        nodes.className = "img-responsive center-block";
        nodes.src = '/static/images/' + data.images[i];
        imagesItem.appendChild(nodes);
        sliderImage.appendChild(imagesItem);
        $('.carousel .item:first').addClass(' active');
    }
    var contentTable = "";
    tableContent.innerHTNL = "";
    for(var r=0; r<data.feature_table.length; r++){
        contentTable += "<tr>";
        for(var c=0; c<data.feature_table[r].length; c++){
            contentTable += "<td>"+data.feature_table[r][c]+"</td>";
        }
        contentTable += "</tr>";
    }
    tableContent.innerHTML = contentTable;
}

function viewCommnts(data){
    scrollCommentDiv.innerHTML = "";
    for(var i=0; i<data.length; i++){
        var commentContent = document.createElement('div');
        var commentPerson = document.createElement('h3');
        var commentComment = document.createElement('p');
        commentContent.className = "comment_content";
        commentPerson.className = "persons";
        commentComment.className = "comments";
        commentPerson.innerHTML = data[i].name;
        commentComment.innerHTML = data[i].comment;
        commentContent.appendChild(commentPerson);
        commentContent.appendChild(commentComment);
        scrollCommentDiv.appendChild(commentContent);
    }
}