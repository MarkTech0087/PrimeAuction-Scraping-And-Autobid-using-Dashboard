from flask import Flask, jsonify, request, render_template, url_for, redirect
import subprocess
import json
import os
import shlex
import requests
from threading import Thread

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    rows_html = request.args.get('rows_html', '')
    keyword = request.args.get('keyword', '').lower()
    with open('1.json') as f:
        auctions = json.load(f)
    
    if keyword == '':
        for idx, auction_info in enumerate(auctions[::-1]):
            product_items = auction_info['product_items']            
            rows_html += f"""
                <tr style="height:40px;">
                    <td rowspan={len(product_items)}>{idx + 1}</td>
                    <th style="text-align:center;" rowspan={len(product_items)}>{auction_info['auction_name']}</th>
                    <td><input type="checkbox" name="account" value="{1}" style="width: 20px; height: 20px;"></td>
                    <td>{product_items[0]['item_title']}</td>
                    <td style="font-size: 14px;">{product_items[0]['product_detail']}</td>
                    <td>{product_items[0]['current_bid_amount']}</td>
                    <td>{product_items[0]['auction_status']}</td>
                    <td style="padding: 0; width: 15%;">
                        <div style="display:flex; justify-content: space-around;">
                            <a style="width: 100%; height: 100%; padding:10 0; text-align: center; cursor:pointer; border-right: 1px solid #dddddd; color:#00732d"
                                onclick="runScript(
                                                '{product_items[0]['item_url']}' 
                                            )"><span class="glyphicon glyphicon-play"></span> Bid</a>

                            <div style="width: 100%; padding: 10px 0; text-align: center; cursor:pointer; border: 0; color: #a5150b"
                                onclick="delAccount('{ auction_info['auction_name'] }')">
                                <span class="glyphicon glyphicon-trash"></span> Delete
                            </div>
                        </div>
                    </td>
                </tr>"""
            
            for idp, product_item in enumerate(product_items[1:]):
                rows_html += f"""
                    <tr>
                        <td><input type="checkbox" name="account" value="{idp+2}" style="width: 20px; height: 20px;"></td>
                        <td>{product_item['item_title']}</td>
                        <td style="font-size: 14px;">{product_item['product_detail']}</td>
                        <td>{product_item['current_bid_amount']}</td>
                        <td>{product_item['auction_status']}</td>
                        <td style="padding: 0; width: 15%;">
                            <div style="display:flex; justify-content: space-around;">
                                <a style="width: 100%; padding:10 0; text-align: center; cursor:pointer; border-right: 1px solid #dddddd; color:#00732d"
                                    onclick="runScript(
                                                    '{product_item['item_url']}' 
                                                )"><span class="glyphicon glyphicon-play"></span> Bid</a>

                                <div style="width: 100%; padding: 10px 0; text-align: center; cursor:pointer; border: 0; color: #a5150b"
                                    onclick="delAccount('{ auction_info['auction_name'] }')">
                                    <span class="glyphicon glyphicon-trash"></span> Delete
                                </div>
                            </div>
                        </td>
                    </tr>
            """
    else:
        rows_html = ""
        print(keyword)
        total = 0
        for idx, auction_info in enumerate(auctions[::-1]):
            product_items = [product_item for product_item in auction_info['product_items'] if keyword in product_item['product_detail'].lower()]
            total += len(product_items)
            if(len(product_items) != 0):
                rows_html += f"""
                <tr style="height:40px;">
                    <td rowspan={len(product_items)}>{idx + 1}</td>
                    <th style="text-align:center;" rowspan={len(product_items)}>{auction_info['auction_name']}</th>
                    <td><input type="checkbox" name="account" value="{1}" style="width: 20px; height: 20px;"></td>
                    <td>{product_items[0]['item_title']}</td>
                    <td style="font-size: 14px;">{product_items[0]['product_detail']}</td>
                    <td>{product_items[0]['current_bid_amount']}</td>
                    <td>{product_items[0]['auction_status']}</td>
                    <td style="padding: 0; width: 15%;">
                        <div style="display:flex; justify-content: space-around;">
                            <a style="width: 100%; height: 100%; padding:10 0; text-align: center; cursor:pointer; border-right: 1px solid #dddddd; color:#00732d"
                                onclick="runScript( 
                                                '{product_items[0]['item_url']}'  
                                            )"><span class="glyphicon glyphicon-play"></span> Bid</a>

                            <div style="width: 100%; padding: 10px 0; text-align: center; cursor:pointer; border: 0; color: #a5150b"
                                onclick="delAccount('{ auction_info['auction_name'] }')">
                                <span class="glyphicon glyphicon-trash"></span> Delete
                            </div>
                        </div>
                    </td>
                </tr>"""
            
                for idp, product_item in enumerate(product_items[1:]):
                    rows_html += f"""
                    <tr>
                        <td><input type="checkbox" name="account" value="{idp+2}" style="width: 20px; height: 20px;"></td>
                        <td>{product_item['item_title']}</td>
                        <td style="font-size: 14px;">{product_item['product_detail']}</td>
                        <td>{product_item['current_bid_amount']}</td>
                        <td>{product_item['auction_status']}</td>
                        <td style="padding: 0; width: 15%;">
                            <div style="display:flex; justify-content: space-around;">
                                <a style="width: 100%; padding:10 0; text-align: center; cursor:pointer; border-right: 1px solid #dddddd; color:#00732d"
                                    onclick="runScript(
                                                    '{product_item['item_url']}'
                                                )"><span class="glyphicon glyphicon-play"></span> Bid</a>

                                <div style="width: 100%; padding: 10px 0; text-align: center; cursor:pointer; border: 0; color: #a5150b"
                                    onclick="delAccount('{ auction_info['auction_name'] }')">
                                    <span class="glyphicon glyphicon-trash"></span> Delete
                                </div>
                            </div>
                        </td>
                    </tr>
            """
        if (total == 0):
            rows_html = f"""
                <tr>
                    <th colspan="8">NO AUCTION FOUND</th>
                </tr>
            """
    print(rows_html)
    return render_template("dashboard.html", rows_html=rows_html)

running_processes = {}

@app.route("/run-script", methods=["POST"])
def run_script():
    try:
        json_data = request.get_json()
        item_url = json_data.get("item_url")
        
        # if os.path.isfile(f"stop-{bet365_username}.flag"):
        #     os.remove(f"stop-{bet365_username}.flag")
        
        process = subprocess.Popen(["python", "bid.py", item_url ])
        print(item_url)
        running_processes[item_url] = process
        
        return jsonify(status="success", message=f"Bid started to {item_url}")
    
    except Exception as e:
        return jsonify(status="error", message=str(e)), 500

@app.route("/delete-account", methods=["POST"])
def delete_account():
    try:
        data = request.get_json()
        bet365_username = data['bet365_username']
        
        if os.path.exists("1.json"):
            with open("1.json", "r") as f:
                accounts = json.load(f)
            
            updated_accounts = [item for item in accounts if item.get("bet365_username") != bet365_username]
            
            with open("1.json", "w") as f:
                json.dump(updated_accounts, f)
            
            return jsonify(status="success", message="Account deleted successfully!")
        else:
            return jsonify(status="error", message="File does not exist")
    
    except Exception as e:
        return jsonify(status="error", message=str(e)), 500

# @app.route("/search", methods=["POST"])
# def search():
#     try:
#         data = request.get_json()
#         keyword = data['keyword'].lower()
#         return redirect(url_for("index", rows_html="", keyword=keyword))
#     except Exception as e:
#         return jsonify(status="error", message=str(e)), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)