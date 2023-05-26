# linguae-dharmae-backend
Code that runs the translation system at linguae-dharmae.net  
This requires a separate inference model: https://github.com/sebastian-nehrdich/mitra-inference/tree/main
## Running LD backend 
`docker build -t linguae-dharmae-backend .   
`docker run -p 3400:80 linguae-dharmae-backend
