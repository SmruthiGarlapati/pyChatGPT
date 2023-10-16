from tkinter import *
import customtkinter
import openai
import openapi
import os
import pickle


#submit to ChatGPT
def speak():
	if gpt_entry.get():
		try:

			gpt_text.delete(1.0, END)

			keyvalue = get_key("api_key_store")


			#gpt_text.insert(END,keyvalue)
			###Query ChatGPT with the entry
			#Define our API Key to ChatGPT
			openai.api_key = keyvalue

			gpt_text.insert(END, f" ...Working..\n")
			#create an instance
			openai.Model.list()

			response = openai.Completion.create(
				model="text-davinci-003",
				prompt= gpt_entry.get(),
				temperature=0,
				max_tokens=60,
				top_p=1.0,
				frequency_penalty=0.0,
				presense_penalty=0.0
				)

			gpt_text.insert(END, response)
			gpt_text.insert(END, "\n\n")

		except Exception as e:
			#Tkinter.messagebox.showerror(title="Error", message=f"\n No Key Found {e}")
			gpt_text.insert(END, f"Error Response {e}")
		finally:
			pass


	else:
		gpt_text.insert(END, "\n\n You did not enter any question 14")


#clear the screen
def clear():
	#clear the main text box
	gpt_text.delete(1.0, END)
	#clear the entry widget
	gpt_entry.delete(0,END)

#call API input stuff
def key():
	#resize app
	root.geometry('600x750')
	#reshow api frame
	api_frame.pack(pady=30)

	#Define a filename for the key
	filename = "api_key_store"

	if os.path.isfile(filename):
		#this file exists, so open and read into the key entry
		input_file = open(filename,"rb")
		#load the data into a variable
		api_entry.delete(0, len(api_entry.get()))

		try:
			keydata = pickle.load(input_file)
			#populate the key entry with the keydata
			
			api_entry.insert(END, keydata)
		except Exception as e:
			Tkinter.messagebox.showerror(title="Error", message=f"\nNo Key Found {e}")
			pass
			#raise
		else:
			pass
		finally:
			pass		
	else:
		# create the input file 
		input_file = open(filename,"wb")
		#close it and later write the key to it
		input_file.close()

#call API stuff
def save_key():

	#open our api_key_store file and write the key to it
	#before writing make sure we have some value for the key
	filename = "api_key_store"
	
	if(len(api_entry.get()) > 0): 

		output_file = open(filename, "wb")
		#write the data to the file
		pickle.dump(api_entry.get(), output_file)


	else:
		messagebox.showerror("ShowError", "No Key Information found")
		pass





	#hide api frame
	api_frame.pack_forget()

	#resize app
	root.geometry('600x600')

def get_key(filename):
	keyvalue = ''
	
		
	try:
		if os.path.isfile(filename):
			#this file exists, so open and read into the key entry
			input_file = open(filename,"rb")
			keyvalue = pickle.load(input_file)
		else:
			return keyvalue

	except Exception as e:
		raise
	finally:
		return keyvalue		
	

	




root = customtkinter.CTk()
root.title("ChatGPT BOT")
root.geometry('600x550')
root.iconbitmap('ai_lt.ico')
#set color scheme
customtkinter.set_appearance_mode("dark")

#add a text box for response from OpenAI
text_frame = customtkinter.CTkFrame(root)
text_frame.pack(pady=20)

gpt_text = Text(text_frame,
	bg="#343638",
	width=65,
	bd=1,
	fg="#d6d6d6",
	relief="flat",
	wrap=WORD,
	selectbackground="#1f538d"
	)

gpt_text.grid(row=0,column=0)

# create a text scroll for the gpt_text
gpt_scroll = customtkinter.CTkScrollbar(text_frame, 
		command=gpt_text.yview)

gpt_scroll.grid(row=0, column=1,sticky="ns")

gpt_text.configure(yscrollcommand=gpt_scroll.set)


#create entry box for the question to ChatGPT
gpt_entry = customtkinter.CTkEntry(root,
	placeholder_text="Type your question to ChatGPT..",
	width=535,
	height=50,
	border_width=1)

gpt_entry.pack(pady=10)

#create button frame for buttons
button_frame = customtkinter.CTkFrame(root, fg_color='#242424')
button_frame.pack(pady=10)

#create buttons
#submit button
submit_button = customtkinter.CTkButton(button_frame,
	text='Talk to ChatGPT',
	command=speak)
submit_button.grid(row=0,column=0, padx=25)

#clear button
clear_button = customtkinter.CTkButton(button_frame,
	text='Clear Response',
	command=clear)
clear_button.grid(row=0,column=1, padx=35)

#api button
api_button = customtkinter.CTkButton(button_frame,
	text='Update API Key',
	command=key)
api_button.grid(row=0,column=2, padx=45)

#api frame for entering api key
api_frame = customtkinter.CTkFrame(root,border_width=1)
api_frame.pack(pady=10)

api_entry = customtkinter.CTkEntry(api_frame,
	placeholder_text="Enter your API Key",
	width=350, height=50, border_width=1)
api_entry.grid(row=0,column=0,padx=20,pady=20)

#Add api save button
api_save_button=customtkinter.CTkButton(api_frame,
	text="Save Key",
	command=save_key)

api_save_button.grid(row=0,column=1,padx=10)

root.mainloop()
