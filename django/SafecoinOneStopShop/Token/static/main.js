
var Token = document.getElementById("sec-33e8");
Token.style.display = "none";
var NFT = document.getElementById("sec-353e");
NFT.style.display = "none";
	
function WalletCheck(){
if(!localStorage.getItem('Keypair')) {
	$("#walletpopup").show();
	console.log('wallet popup');
  //popupWindow = window.open(
//		'WalletPopup/','popUpWindow','height=300,width=400,left=10,top=10,resizable=yes,scrollbars=yes,toolbar=yes,menubar=no,location=no,directories=no,status=yes')
  //populateKeypair();
} else {
  setKeypair();
  
}
}


function CreateWallet() {
  /*get new key and save client side*/
  $("#walletpopup").hide();
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  $.ajax({
	  headers: {'X-CSRFToken': csrftoken},
   type: "GET",
   url: "WalletNew/",
   data: {},
   success: function callback(response){
               //console.log(response);
			   localStorage.setItem('Keypair', response);
			   //var btn = document.getElementById("WalletBtn");
			   //btn.innerText=response;
			   //document.getElementById("WalletBtn").value=;
            }
});
  
  //save
  setKeypair()
  console.log('Wallet Saved');

}

function ImportWallet(){
	$("#walletpopup").hide();
	const val = document.getElementById('importKeypair').value;
	//console.log(val);
	localStorage.setItem('Keypair', val);
	setKeypair()
}



function setKeypair() {
  var currentKey = localStorage.getItem('Keypair');/*get client stored keypair*/
  console.log(currentKey)
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
 $.ajax({
	 headers: {'X-CSRFToken': csrftoken},
   type: "POST",
   url: 'Wallet/',
   data: {'keypair':currentKey},
   success: function callback(response){
               console.log(response);
			   var btn = document.getElementById("WalletBtn");
			   btn.innerText=response;
			   //document.getElementById("WalletBtn").value=response;
            }
});
  /*document.getElementById('Keypair').value = currentColor;*/
}

function HomePage(){
	var Home = document.getElementById("sec-fb3f");
	Home.style.display = "block";
	var Token = document.getElementById("sec-33e8");
	Token.style.display = "none";
	var NFT = document.getElementById("sec-353e");
	NFT.style.display = "none";
	
}
function TokenPage(){
	var Home = document.getElementById("sec-fb3f");
	Home.style.display = "none";
	var Token = document.getElementById("sec-33e8");
	Token.style.display = "block";
	var NFT = document.getElementById("sec-353e");
	NFT.style.display = "none";
	
}
function NFTPage(){
	var Home = document.getElementById("sec-fb3f");
	Home.style.display = "none";
	var Token = document.getElementById("sec-33e8");
	Token.style.display = "none";
	var NFT = document.getElementById("sec-353e");
	NFT.style.display = "block";
	console.log('NFT');
	
}

	
function NewToken() {
  /*get new key and save client side*/
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  $.ajax({
	  headers: {'X-CSRFToken': csrftoken},
   type: "GET",
   url: "NewToken/",
   data: {},
   success: function callback(response){
               console.log(response);
			   //var btn = document.getElementById("WalletBtn");
			   //btn.innerText=response;
			   //document.getElementById("WalletBtn").value=;
            }
});

}
