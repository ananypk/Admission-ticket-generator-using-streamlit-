import pandas as pd
import streamlit as st
import pdfkit

file1=pd.read_csv() #file path here
size=list(file1.shape)


def rollnum(x):
  roll_num_list=list(file1.at[x,'srn'])
  roll_num=int(roll_num_list[9])*1000+int(roll_num_list[10])*100+int(roll_num_list[11])*10+int(roll_num_list[12])
  return(roll_num)


def seat(x):
  room_no=int(x/60)
  seat_no=x%60
  return(room_no, seat_no)
st.title('University Exam Admssion Ticket')


with st.form(key='myform',clear_on_submit=True):
    name=st.text_input("Name: ")
    srn1=st.text_input("SRN: ")
    submitb=st.form_submit_button("Submit")

if submitb:
    a=-1
    for i in file1['name']:
        a=a+1
        if i.lower()==name.lower():
            if file1.at[a,'srn'] == srn1:
                print(srn1)
                roll_num_list=list(file1.at[a,'srn'])
                roll_num=int(roll_num_list[9])*1000+int(roll_num_list[10])*100+int(roll_num_list[11])*10+int(roll_num_list[12])
                room_no=int(roll_num/60)
                seat_no=roll_num%60
                st.write("Name: ", file1.at[a,'name'])
                st.write('SRN: ',file1.at[a,'srn'])
                if file1.at[a,'attendance']>=85:
                    if file1.at[a,'certificate']=='YES':
                        t1={}
                        for x in range(1,7):
                            t1["Name"]=file1.at[a,'name']
                            t1["SRN"]=file1.at[a,'srn']
                            t1["Course"]=file1.at[a,'course']
                            t1["Semister"]=file1.at[a,'sem']
                            t1["Class"]=file1.at[a,'class']
                            t1["Roll number"]=roll_num
                            t1["Room number"]=room_no
                            t1["Seat number"]=seat_no
                        d1 = pd.DataFrame(list(t1.items()))
                        html_file1=d1.to_html('et.html')
                        path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
                        config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
                        new=pdfkit.from_file('et.html', 'exam_hallticket.pdf',configuration=config)
                        st.success('All requirements are met.')
                        st.header("Hall Ticket")
                        st.table(d1)
                        with open("exam_hallticket.pdf",'rb') as pdf_file:
                            PDFbyte=pdf_file.read()
                        st.download_button(label="Download data as Pdf", data=PDFbyte, file_name='exam_hallticket.pdf', mime='application/octet-stream')
                        break
                    else:
                        st.error("Permission denied. Certificates not submitted.")
                        break
                else:
                    st.error("Permission denied. Attendance too low.")
                    break
            else:
                st.error("wrong srn")
                break
        elif a==size[0]-1:
            st.error("Error, not found.")