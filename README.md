# final_year_project
This is the space to deposit the final year CS project.

# data_organisation
In the submission, a python file, a txt file, and the number of dataset have been delivered. <br/> 
The dataset were captured by Wireshark and collected by bgth83. <br/> 
Raw packet captured files using Wireshark have been delivered in the submission, and the dataset have been captured by bgth83.<br/> 
The raw network packets captured files from four ISPs including three British ISPs and a Korean ISP. <br/> 
- Participated British ISPs - BT, Vodafone, Virgin media
- Participated Korean ISP - KT
 
A folder named “PCAP_BT” in pcap files folder contains 25 Wireshark capture files(.pcapng) from BT, employed applications are WhatsApp, YouTube, YouTube music, Spotify, MS Outlook, Kakaotallk, imessage, Zoom and Facetime.<br/> 
<br/> 
A folder named “PCAP_VirginMedia” in "pcap files" folder contains 17 Wireshark capture files(.pcapng) from Virgin media, used applications are Teams, MS Outlook, Spotify, WhatsApp, Kakaotalk and YouTube. <br/> 
<br/> 
A folder named “PCAP_Vodafone” in "pcap files" folder includes 19 Wireshark capture files(.pcapng) from Vodafone, employed applications are imessage, Kakaotalk, MS Outlook, Spotify, Teams, Facetime, WhatsApp, YouTube, YouTube music and Zoom. <br/> 
<br/> 
A folder named “PCAP_KT” in "pcap files" folder contains 7 Wireshark capture files(.pcapng) from KT, used applications are Discord, Gmail, MS Outlook, YouTube, YouTube music and KakaoTalk. <br/> <br/> 
The folder named “PCAP_project_applied_packet” in "pcap files" folder includes four .pcapng files which have been applied to the final paper for the performance matrices and the four .pcapng files in the folder are based on UDP applications.<br/> <br/> 
The python file in "python files" folder, “code_implementation.py” is a software tool that facilitates performance evaluation and analysis. <br/> <br/>
Also, "reports" folder includes the final project paper.
* Note : raw data files for youtube and youtube music.pcapng in "PCAP_KT", and a raw datafile kt.pcapng in "PCAP_project_applied_packet" haven't been uploaded successfully on git due to file size issue, however; it has been uploaded on Ultra. *

# code_implementation
This is the instruction of “code_implementation.py”.

#################################################################################### <br/> 
This is a command line application, to execute it, please open the terminal (MAC) or, CMD(Windows).<br/> <br/> 

The application has 4 main functions.<br/> 
1. Identify coexistence method - is going to tell you the deployed coexistence method.<br/> 
2. Analyse Packet Data (IPv4) - is going to analyse the performance of the ISP by taking user input (src and dst addresses - IPv4).<br/> 
3. Analyse Packet Data (IPv6) - is going to analyse the performance of the ISP by taking user input (src and dst addresses - IPv6).<br/> 
4. Analyse IPv6 Usage - is going to display the total frame numbers and total number of IPv6 addresses with a visualisation.<br/> <br/> 

Then, please make sure, you are in the right directory. - /code_submission<br/> 
You can run the application by typing python3 code_implementation.py on the command line.<br/> 
If you encounter any errors, you can also execute it on visual studio code easily.<br/> <br/> 

To load the packet files, you need to input the path and filename.<br/> 
For example, project_applied_packet/bt.pcapng<br/> <br/> 

Then, please choose the option you want to execute.<br/> <br/> 


the final paper is based on packets in a folder, project_applied_packet. <br/> 
####################################################################################




