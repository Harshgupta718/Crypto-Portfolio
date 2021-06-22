from tkinter import *
from tkinter import messagebox, Menu
import requests
import json
import sqlite3

root = Tk()
root.title("Crpto Portfolio")
con = sqlite3.connect('coin.db')
cursorObj = con.cursor()
cursorObj.execute("CREATE TABLE IF NOT EXISTS coin(id INTEGER PRIMARY KEY, symbol TEXT, amount INTEGER, price REAL)")
con.commit()

def app_header():

	header_pi = Label(root, text =  "Portfolio ID", bg = "#142E54", fg = "white", font = "Verdana 12 bold", borderwidth = 2, relief = "groove", padx = "2", pady = "2")
	header_pi.grid(row = 0, column = 0, sticky = N + S + E + W) 
	header_name = Label(root, text =  "Coin Name", bg = "#142E54", fg = "white", font = "Verdana 12 bold", borderwidth = 2, relief = "groove", padx = "2", pady = "2")
	header_name.grid(row = 0, column = 1, sticky = N + S + E + W) 
	header_cp = Label(root, text =  "Total Amount Paid", bg = "#142E54", fg = "white" , font = "Verdana 12 bold", borderwidth = 2, relief = "groove", padx = "2", pady = "2")
	header_cp.grid(row = 0, column = 2, sticky = N + S + E + W) 
	header_cp = Label(root, text =  "Coins Owned", bg = "#142E54", fg = "white" , font = "Verdana 12 bold", borderwidth = 2, relief = "groove", padx = "2", pady = "2")
	header_cp.grid(row = 0, column = 3, sticky = N + S + E + W) 
	header_pp = Label(root, text =  "Price", bg = "#142E54", fg = "white", font = "Verdana 12 bold", borderwidth = 2, relief = "groove", padx = "2", pady = "2")
	header_pp.grid(row = 0, column = 4, sticky = N + S + E + W) 
	header_cv = Label(root, text =  "Current Value", bg = "#142E54", fg = "white", font = "Verdana 12 bold", borderwidth = 2, relief = "groove", padx = "2", pady = "2")
	header_cv.grid(row = 0, column = 5, sticky = N + S + E + W) 
	header_pl_per = Label(root, text =  "P/L Per Coin", bg = "#142E54", fg = "white", font = "Verdana 12 bold", borderwidth = 2, relief = "groove", padx = "2", pady = "2")
	header_pl_per.grid(row = 0, column = 6, sticky = N + S + E + W) 
	header_pl_total = Label(root, text =  "Total P/L", bg = "#142E54", fg = "white", font = "Verdana 12 bold", borderwidth = 2, relief = "groove", padx = "2", pady = "2")
	header_pl_total.grid(row = 0, column = 7, sticky = N + S + E + W) 

def reset():
	for cell in root.winfo_children():
		cell.destroy()

	app_nav()
	app_header()
	lookup()

def app_nav():
	def clear_all():
		cursorObj.execute("DELETE FROM coin")
		con.commit()

		messagebox.showinfo("Portfolio Notification", "Portfolio Cleared - Add New Coins")
		reset()

	def close_all():
		root.destroy()

	menu = Menu(root)
	file_item = Menu(menu)
	file_item.add_command(label = "Clear Portfolio", command = clear_all)
	file_item.add_command(label = "Close App", command = close_all)
	menu.add_cascade(label = "File", menu = file_item)
	root.config(menu = menu)

def lookup():
	api_request = requests.get("https://api.wazirx.com/api/v2/tickers")
	api = json.loads(api_request.content) 
	
	cursorObj.execute("SELECT * FROM coin")
	portfolio = cursorObj.fetchall()

	def insert_coin():
		cursorObj.execute("INSERT INTO coin(symbol, price, amount) VALUES(?, ?, ?)", (symbol_txt.get(), price_paid_txt.get(), amount_txt.get()))
		con.commit()
		messagebox.showinfo("Portfolio Notification", "Coin Added Successfully")
		reset()

	def update_coin():
		cursorObj.execute("UPDATE coin SET symbol = ?, price = ?, amount = ? WHERE id = ?", (symbol_update.get(), price_paid_update.get(), amount_update.get(), portid_update.get()))
		con.commit()
		messagebox.showinfo("Portfolio Notification", "Coin Updated Successfully")
		reset()

	def delete_coin():
		cursorObj.execute("DELETE FROM coin WHERE id = ?", (portid_delete.get(), ))
		con.commit()
		messagebox.showinfo("Portfolio Notification", "Coin Deleted")
		reset()

	def red_green(amount):
		if amount >= 0:
			return "green"
		else:
			return "red"

	# import pdb
	# pdb.set_trace()

	portfolio_total = 0 
	total_amount_paid = 0
	total_current_value = 0
	row_count = 1
	for x in api:
		for coin in portfolio:
			if coin[1] == api[x]["base_unit"] and api[x]["quote_unit"] == "inr":

				#Do_some_math
				total_paid = float(coin[3])
				current_value = coin[2] * float(api[x]["last"])
				profit_loss_per_coin = (current_value - total_paid) / coin[2]
				portfolio_total_per_coin = current_value - total_paid
				portfolio_total += portfolio_total_per_coin
				total_amount_paid += total_paid
				total_current_value += current_value

				pi = Label(root, text = coin[0], bg = "#F3F4F6", fg = "black", borderwidth = 2, relief = "groove", padx = "2", pady = "2")
				pi.grid(row = row_count, column = 0, sticky = N + S + E + W) 
				
				name = Label(root, text = api[x]["base_unit"], bg = "#F3F4F6", fg = "black", borderwidth = 2, relief = "groove", padx = "2", pady = "2")
				name.grid(row = row_count, column = 1, sticky = N + S + E + W) 
				
				cp = Label(root, text = ("{0:.6f}".format(float(total_paid))).rstrip('0').rstrip('.'), bg = "#F3F4F6", fg = "black", borderwidth = 2, relief = "groove", padx = "2", pady = "2")
				cp.grid(row = row_count, column = 2, sticky = N + S + E + W) 
				
				co = Label(root, text = ("{0:.6f}".format(float(coin[2]))).rstrip('0').rstrip('.'), bg = "#F3F4F6", fg = "black", borderwidth = 2, relief = "groove", padx = "2", pady = "2")
				co.grid(row = row_count, column = 3, sticky = N + S + E + W) 
				
				pp = Label(root, text = ("{0:.6f}".format(float(api[x]["last"]))).rstrip('0').rstrip('.'), bg = "#F3F4F6", fg = "black", borderwidth = 2, relief = "groove", padx = "2", pady = "2")
				pp.grid(row = row_count, column = 4, sticky = N + S + E + W) 
				
				cv = Label(root, text = ("{0:.6f}".format(float(current_value))).rstrip('0').rstrip('.'), bg = "#F3F4F6", fg = "black", borderwidth = 2, relief = "groove", padx = "2", pady = "2")
				cv.grid(row = row_count, column = 5, sticky = N + S + E + W) 
				
				pl_per = Label(root, text = ("{0:.6f}".format(float(profit_loss_per_coin))).rstrip('0').rstrip('.'), bg = "#F3F4F6", fg = red_green(float(profit_loss_per_coin)), borderwidth = 2, relief = "groove", padx = "2", pady = "2")
				pl_per.grid(row = row_count, column = 6, sticky = N + S + E + W) 
				
				pl_total = Label(root, text = ("{0:.6f}".format(float(portfolio_total_per_coin))).rstrip('0').rstrip('.'), bg = "#F3F4F6", fg = red_green(float(portfolio_total_per_coin)), borderwidth = 2, relief = "groove", padx = "2", pady = "2")
				pl_total.grid(row = row_count, column = 7, sticky = N + S + E + W) 
				
				row_count += 1

	#insert_data
	symbol_txt = Entry(root, borderwidth = 2, relief = "groove")
	symbol_txt.grid(row = row_count + 1, column = 1)

	price_paid_txt = Entry(root, borderwidth = 2, relief = "groove")
	price_paid_txt.grid(row = row_count + 1, column = 2)

	amount_txt = Entry(root, borderwidth = 2, relief = "groove")
	amount_txt.grid(row = row_count + 1, column = 3)

	add_coin = Button(root, text = "Add Coin", command = insert_coin, bg = "#142E54", fg = "white", font = "Verdana 12 bold", borderwidth = 2, relief = "groove", padx = "2", pady = "2")
	add_coin.grid(row  = row_count + 1, column = 4, sticky = N + S + E + W)

	#update_data
	portid_update = Entry(root, borderwidth = 2, relief = "groove")
	portid_update.grid(row = row_count + 2, column = 0)

	symbol_update = Entry(root, borderwidth = 2, relief = "groove")
	symbol_update.grid(row = row_count + 2, column = 1)

	price_paid_update = Entry(root, borderwidth = 2, relief = "groove")
	price_paid_update.grid(row = row_count + 2, column = 2)

	amount_update = Entry(root, borderwidth = 2, relief = "groove")
	amount_update.grid(row = row_count + 2, column = 3)

	update_coin = Button(root, text = "Update Coin", command = update_coin, bg = "#142E54", fg = "white", font = "Verdana 12 bold", borderwidth = 2, relief = "groove", padx = "2", pady = "2")
	update_coin.grid(row  = row_count + 2, column = 4, sticky = N + S + E + W)

	#delete_data
	portid_delete = Entry(root, borderwidth = 2, relief = "groove")
	portid_delete.grid(row = row_count + 3, column = 0)

	delete_coin = Button(root, text = "Delete Coin", command = delete_coin, bg = "#142E54", fg = "white", font = "Verdana 12 bold", borderwidth = 2, relief = "groove", padx = "2", pady = "2")
	delete_coin.grid(row  = row_count + 3, column = 4, sticky = N + S + E + W)


	portfolio_profits = Label(root, text = ("{0:.6f}".format(float(portfolio_total))).rstrip('0').rstrip('.'), font = "Verdana 8 bold", bg = "#F3F4F6", fg = red_green(float(portfolio_total)), borderwidth = 2, relief = "groove", padx = "2", pady = "2")
	portfolio_profits.grid(row = row_count, column = 7, sticky = N + S + E + W)
	
	total_ap = Label(root, text = ("{0:.6f}".format(float(total_amount_paid))).rstrip('0').rstrip('.'), font = "Verdana 8 bold", bg = "#F3F4F6", fg = "black", borderwidth = 2, relief = "groove", padx = "2", pady = "2")
	total_ap.grid(row = row_count, column = 2, sticky = N + S + E + W)
	
	total_cv = Label(root, text = ("{0:.6f}".format(float(total_current_value))).rstrip('0').rstrip('.'), font = "Verdana 8 bold", bg = "#F3F4F6", fg = "black", borderwidth = 2, relief = "groove", padx = "2", pady = "2")
	total_cv.grid(row = row_count, column = 5, sticky = N + S + E + W)

	api = ""
	refresh_button = Button(root, text = "Refresh", command = reset, bg = "#142E54", fg = "white", font = "Verdana 12 bold", borderwidth = 2, relief = "groove", padx = "2", pady = "2")
	refresh_button.grid(row  = row_count + 1, column = 7, sticky = N + S + E + W)

app_nav()
app_header()
lookup()
root.mainloop()

cursor.close()
con.close()