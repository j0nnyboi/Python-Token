
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
               console.log(response);
			   localStorage.setItem('Keypair', response['seed']);
			   //var btn = document.getElementById("WalletBtn");
			   //btn.innerText=response;
			   //document.getElementById("WalletBtn").value=;
			   var btn = document.getElementById("WalletBtn");
					btn.innerText=response['pubkey'];
				BalanceShow()
            }
});
  
  //save
  console.log('Wallet Saved');
 

}

function ImportWallet(){
	$("#walletpopup").hide();
	const val = document.getElementById('importKeypair').value;
	//console.log(val);
	localStorage.setItem('Keypair', val);
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
			   BalanceShow()
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

var main = document.getElementById('Mainnet');
var test = document.getElementById('Testnet');
var dev = document.getElementById('Devnet');
main.style.color = '#6bf2b3'; 
test.style.color = '#000000';  
dev.style.color = '#000000';  
						
function Chain(chain){
	//console.log("chain change");
	//console.log(chain);
	 const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  $.ajax({
	  headers: {'X-CSRFToken': csrftoken},
   type: "POST",
   url: "ChangeChain/",
   data: {'chain':chain},
   success: function callback(response){
                var main = document.getElementById('Mainnet');
			    var test = document.getElementById('Testnet');
				var dev = document.getElementById('Devnet');
				if(response['endpoint'] == 'Connection Error Mainnet'){
					main.style.color = '#FF0000'; 
					test.style.color = '#000000';  
					dev.style.color = '#000000'; 
					alert(response['endpoint']);
					document.getElementById("walletBalance").innerHTML = 0;
				}else if(response['endpoint'] == 'Connection Error Testnet'){
					main.style.color = '#000000'; 
					test.style.color = '#FF0000';  
					dev.style.color = '#000000';
					alert(response['endpoint']);
					document.getElementById("walletBalance").innerHTML = 0;
				}else if(response['endpoint'] == 'Connection Error Devnet'){
					main.style.color = '#000000'; 
					test.style.color = '#000000';  
					dev.style.color = '#FF0000';
					alert(response['endpoint']);
					document.getElementById("walletBalance").innerHTML = 0;
				
				}else{
					console.log(response['endpoint']);
					BalanceShow()
					if(chain == 'Mainnet'){
						main.style.color = '#6bf2b3'; 
						test.style.color = '#000000';  
						dev.style.color = '#000000';  					
					}else if (chain == 'Testnet'){
						main.style.color = '#000000'; 
						test.style.color = '#6bf2b3';  
						dev.style.color = '#000000';
				}else if (chain == 'Devnet'){
						main.style.color = '#000000'; 
						test.style.color = '#000000';  
						dev.style.color = '#6bf2b3';
				}
            }
   }
});
	
	
}

function BalanceShow(){
	const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  $.ajax({
	  headers: {'X-CSRFToken': csrftoken},
   type: "POST",
   url: "Balance/",
   data: {},
   success: function callback(response){
	document.getElementById("walletBalance").innerHTML = response['bal'];
	
   }
});
}
