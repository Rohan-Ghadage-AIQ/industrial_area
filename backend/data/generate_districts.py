"""
Generate districts.json — Comprehensive Indian districts dataset with centroids.
Run once: python generate_districts.py
"""

import json
from pathlib import Path

# All Indian districts organized by state with approximate centroids [district, lat, lng]
# Centroids are approximate — used only as search location bias for the API

DISTRICTS_DATA = {
    "Andhra Pradesh": [
        ["Anantapur", 14.68, 77.60], ["Chittoor", 13.22, 79.10], ["East Godavari", 17.00, 81.80],
        ["Guntur", 16.30, 80.44], ["Krishna", 16.57, 80.86], ["Kurnool", 15.83, 78.04],
        ["Nellore", 14.45, 79.99], ["Prakasam", 15.35, 79.56], ["Srikakulam", 18.30, 83.90],
        ["Visakhapatnam", 17.69, 83.22], ["Vizianagaram", 18.11, 83.40],
        ["West Godavari", 16.72, 81.10], ["YSR Kadapa", 14.47, 78.82],
        ["Annamayya", 13.63, 78.73], ["Bapatla", 15.90, 80.47], ["Eluru", 16.71, 81.10],
        ["Kakinada", 16.96, 82.24], ["Konaseema", 16.65, 81.78], ["Nandyal", 15.48, 78.48],
        ["NTR", 16.51, 80.65], ["Palnadu", 16.15, 79.72], ["Parvathipuram Manyam", 18.77, 83.43],
        ["Sri Sathya Sai", 14.16, 77.79], ["Tirupati", 13.63, 79.42],
        ["Alluri Sitharama Raju", 17.62, 81.80], ["Anakapalli", 17.69, 83.00]
    ],
    "Arunachal Pradesh": [
        ["Tawang", 27.59, 91.86], ["West Kameng", 27.23, 92.36], ["East Kameng", 27.13, 93.03],
        ["Papum Pare", 27.17, 93.83], ["Kurung Kumey", 27.83, 93.33],
        ["Lower Subansiri", 27.63, 93.83], ["Upper Subansiri", 28.17, 94.23],
        ["West Siang", 28.06, 94.57], ["East Siang", 28.07, 95.34],
        ["Upper Siang", 28.70, 95.30], ["Changlang", 27.13, 96.33],
        ["Tirap", 27.00, 95.75], ["Lower Dibang Valley", 28.33, 95.85],
        ["Dibang Valley", 28.70, 95.70], ["Lohit", 27.85, 96.25],
        ["Anjaw", 28.07, 96.83], ["Namsai", 27.68, 95.87],
        ["Longding", 26.90, 95.33], ["Kra Daadi", 27.92, 93.58],
        ["Siang", 28.17, 94.87], ["Kamle", 27.73, 93.83],
        ["Lower Siang", 27.95, 94.83], ["Lepa Rada", 28.00, 94.40],
        ["Pakke Kessang", 27.05, 93.00], ["Shi Yomi", 28.22, 94.10],
        ["Itanagar Capital Complex", 27.08, 93.61]
    ],
    "Assam": [
        ["Baksa", 26.70, 91.25], ["Barpeta", 26.32, 91.00], ["Biswanath", 26.73, 93.15],
        ["Bongaigaon", 26.48, 90.55], ["Cachar", 24.82, 92.78], ["Charaideo", 26.97, 94.87],
        ["Chirang", 26.51, 90.22], ["Darrang", 26.51, 92.17], ["Dhemaji", 27.48, 94.58],
        ["Dhubri", 26.02, 90.00], ["Dibrugarh", 27.47, 94.91], ["Dima Hasao", 25.50, 93.02],
        ["Goalpara", 26.17, 90.62], ["Golaghat", 26.52, 93.96], ["Hailakandi", 24.68, 92.57],
        ["Hojai", 26.00, 92.85], ["Jorhat", 26.76, 94.22], ["Kamrup", 26.22, 91.67],
        ["Kamrup Metropolitan", 26.14, 91.74], ["Karbi Anglong", 25.93, 93.47],
        ["Karimganj", 24.87, 92.35], ["Kokrajhar", 26.40, 90.27],
        ["Lakhimpur", 27.24, 94.10], ["Majuli", 26.95, 94.17], ["Morigaon", 26.25, 92.34],
        ["Nagaon", 26.35, 92.68], ["Nalbari", 26.44, 91.44], ["Sivasagar", 26.98, 94.63],
        ["Sonitpur", 26.77, 92.97], ["South Salmara-Mankachar", 25.10, 89.87],
        ["Tinsukia", 27.49, 95.36], ["Udalguri", 26.75, 92.10],
        ["West Karbi Anglong", 25.77, 93.17], ["Bajali", 26.42, 91.07],
        ["Tamulpur", 26.63, 91.45]
    ],
    "Bihar": [
        ["Araria", 26.15, 87.48], ["Arwal", 25.24, 84.69], ["Aurangabad", 24.75, 84.37],
        ["Banka", 24.89, 86.92], ["Begusarai", 25.42, 86.13], ["Bhagalpur", 25.24, 86.97],
        ["Bhojpur", 25.56, 84.45], ["Buxar", 25.57, 83.98], ["Darbhanga", 26.17, 85.90],
        ["East Champaran", 26.65, 84.85], ["Gaya", 24.80, 85.01], ["Gopalganj", 26.47, 84.44],
        ["Jamui", 24.93, 86.22], ["Jehanabad", 25.21, 84.99], ["Kaimur", 25.05, 83.58],
        ["Katihar", 25.54, 87.57], ["Khagaria", 25.50, 86.47], ["Kishanganj", 26.09, 87.95],
        ["Lakhisarai", 25.16, 86.09], ["Madhepura", 25.92, 86.79], ["Madhubani", 26.35, 86.07],
        ["Munger", 25.38, 86.47], ["Muzaffarpur", 26.12, 85.39], ["Nalanda", 25.13, 85.44],
        ["Nawada", 24.89, 85.53], ["Patna", 25.61, 85.14], ["Purnia", 25.78, 87.47],
        ["Rohtas", 24.97, 84.01], ["Saharsa", 25.88, 86.60], ["Samastipur", 25.86, 85.78],
        ["Saran", 25.83, 84.78], ["Sheikhpura", 25.14, 85.84], ["Sheohar", 26.52, 85.30],
        ["Sitamarhi", 26.59, 85.49], ["Siwan", 26.22, 84.36], ["Supaul", 26.12, 86.60],
        ["Vaishali", 25.69, 85.22], ["West Champaran", 26.73, 84.43]
    ],
    "Chhattisgarh": [
        ["Balod", 20.73, 81.20], ["Baloda Bazar", 21.65, 82.16], ["Balrampur", 23.63, 83.53],
        ["Bastar", 19.07, 81.95], ["Bemetara", 21.72, 81.53], ["Bijapur", 18.84, 80.77],
        ["Bilaspur", 22.09, 82.15], ["Dantewada", 18.90, 81.35], ["Dhamtari", 20.71, 81.55],
        ["Durg", 21.19, 81.28], ["Gariaband", 20.63, 82.06], ["Gaurela-Pendra-Marwahi", 22.95, 81.67],
        ["Janjgir-Champa", 22.01, 82.58], ["Jashpur", 22.78, 84.14],
        ["Kabirdham", 22.10, 81.25], ["Kanker", 20.27, 81.10], ["Kondagaon", 19.60, 81.66],
        ["Korba", 22.35, 82.68], ["Koriya", 23.25, 82.55], ["Mahasamund", 21.11, 82.10],
        ["Mungeli", 22.07, 81.68], ["Narayanpur", 19.72, 81.25], ["Raigarh", 21.90, 83.40],
        ["Raipur", 21.25, 81.63], ["Rajnandgaon", 21.10, 81.03], ["Sukma", 18.40, 81.67],
        ["Surajpur", 23.22, 82.87], ["Surguja", 23.12, 83.09], ["Sarangarh-Bilaigarh", 21.59, 82.78],
        ["Khairagarh-Chhuikhadan-Gandai", 21.42, 80.97], ["Mohla-Manpur-Ambagarh Chowki", 20.93, 80.75],
        ["Manendragarh-Chirmiri-Bharatpur", 23.20, 82.18],
        ["Sakti", 22.03, 82.96]
    ],
    "Goa": [
        ["North Goa", 15.53, 73.96], ["South Goa", 15.28, 74.09]
    ],
    "Gujarat": [
        ["Ahmedabad", 23.02, 72.58], ["Amreli", 21.60, 71.22], ["Anand", 22.56, 72.95],
        ["Aravalli", 23.62, 73.22], ["Banaskantha", 24.17, 72.43], ["Bharuch", 21.70, 72.97],
        ["Bhavnagar", 21.76, 72.15], ["Botad", 22.17, 71.67], ["Chhota Udaipur", 22.30, 74.02],
        ["Dahod", 22.84, 74.25], ["Dang", 20.75, 73.68], ["Devbhumi Dwarka", 22.20, 69.08],
        ["Gandhinagar", 23.22, 72.65], ["Gir Somnath", 20.93, 70.50], ["Jamnagar", 22.47, 70.07],
        ["Junagadh", 21.52, 70.46], ["Kutch", 23.73, 69.86], ["Kheda", 22.75, 72.68],
        ["Mahisagar", 23.15, 73.63], ["Mehsana", 23.59, 72.38], ["Morbi", 22.82, 70.83],
        ["Narmada", 21.87, 73.50], ["Navsari", 20.85, 72.92], ["Panchmahal", 22.77, 73.60],
        ["Patan", 23.85, 72.13], ["Porbandar", 21.64, 69.60], ["Rajkot", 22.30, 70.78],
        ["Sabarkantha", 23.62, 73.07], ["Surat", 21.17, 72.83], ["Surendranagar", 22.73, 71.68],
        ["Tapi", 21.15, 73.40], ["Vadodara", 22.30, 73.19], ["Valsad", 20.60, 72.93]
    ],
    "Haryana": [
        ["Ambala", 30.38, 76.78], ["Bhiwani", 28.79, 76.13], ["Charkhi Dadri", 28.59, 76.27],
        ["Faridabad", 28.41, 77.31], ["Fatehabad", 29.52, 75.45], ["Gurugram", 28.46, 77.03],
        ["Hisar", 29.15, 75.72], ["Jhajjar", 28.61, 76.66], ["Jind", 29.32, 76.31],
        ["Kaithal", 29.80, 76.40], ["Karnal", 29.69, 76.98], ["Kurukshetra", 29.97, 76.84],
        ["Mahendragarh", 28.28, 76.15], ["Nuh", 28.10, 77.00], ["Palwal", 28.14, 77.33],
        ["Panchkula", 30.69, 76.86], ["Panipat", 29.39, 76.97], ["Rewari", 28.19, 76.62],
        ["Rohtak", 28.89, 76.57], ["Sirsa", 29.53, 75.02], ["Sonipat", 28.99, 77.02],
        ["Yamunanagar", 30.13, 77.29]
    ],
    "Himachal Pradesh": [
        ["Bilaspur", 31.34, 76.76], ["Chamba", 32.55, 76.13], ["Hamirpur", 31.68, 76.52],
        ["Kangra", 32.10, 76.27], ["Kinnaur", 31.58, 78.17], ["Kullu", 31.96, 77.11],
        ["Lahaul and Spiti", 32.57, 77.04], ["Mandi", 31.72, 76.93], ["Shimla", 31.10, 77.17],
        ["Sirmaur", 30.57, 77.30], ["Solan", 30.91, 77.10], ["Una", 31.47, 76.27]
    ],
    "Jharkhand": [
        ["Bokaro", 23.67, 86.15], ["Chatra", 24.20, 84.87], ["Deoghar", 24.49, 86.70],
        ["Dhanbad", 23.80, 86.43], ["Dumka", 24.27, 87.25], ["East Singhbhum", 22.80, 86.20],
        ["Garhwa", 24.17, 83.80], ["Giridih", 24.19, 86.30], ["Godda", 24.83, 87.22],
        ["Gumla", 23.04, 84.54], ["Hazaribagh", 23.99, 85.36], ["Jamtara", 24.00, 86.80],
        ["Khunti", 23.07, 85.28], ["Koderma", 24.47, 85.59], ["Latehar", 23.74, 84.50],
        ["Lohardaga", 23.44, 84.68], ["Pakur", 24.63, 87.85], ["Palamu", 24.03, 84.08],
        ["Ramgarh", 23.63, 85.56], ["Ranchi", 23.34, 85.31], ["Sahibganj", 25.24, 87.64],
        ["Seraikela Kharsawan", 22.70, 85.83], ["Simdega", 22.62, 84.52],
        ["West Singhbhum", 22.36, 85.83]
    ],
    "Karnataka": [
        ["Bagalkot", 16.18, 75.70], ["Bengaluru Rural", 13.22, 77.71],
        ["Bengaluru Urban", 12.97, 77.59], ["Belagavi", 15.85, 74.50],
        ["Ballari", 15.14, 76.92], ["Bidar", 17.91, 77.52], ["Chamarajanagar", 11.92, 76.94],
        ["Chikballapur", 13.43, 77.73], ["Chikkamagaluru", 13.32, 75.77],
        ["Chitradurga", 14.23, 76.40], ["Dakshina Kannada", 12.87, 75.37],
        ["Davanagere", 14.47, 75.92], ["Dharwad", 15.46, 75.01], ["Gadag", 15.43, 75.63],
        ["Hassan", 13.01, 76.10], ["Haveri", 14.79, 75.40], ["Kalaburagi", 17.33, 76.83],
        ["Kodagu", 12.34, 75.81], ["Kolar", 13.14, 78.13], ["Koppal", 15.35, 76.15],
        ["Mandya", 12.52, 76.90], ["Mysuru", 12.30, 76.64], ["Raichur", 16.21, 77.36],
        ["Ramanagara", 12.72, 77.28], ["Shivamogga", 14.00, 75.57],
        ["Tumakuru", 13.34, 77.10], ["Udupi", 13.34, 74.75], ["Uttara Kannada", 14.79, 74.69],
        ["Vijayapura", 16.83, 75.71], ["Yadgir", 16.77, 77.14], ["Vijayanagara", 15.35, 76.47]
    ],
    "Kerala": [
        ["Alappuzha", 9.49, 76.34], ["Ernakulam", 9.98, 76.28], ["Idukki", 9.85, 76.97],
        ["Kannur", 11.87, 75.37], ["Kasaragod", 12.50, 75.00], ["Kollam", 8.89, 76.60],
        ["Kottayam", 9.59, 76.52], ["Kozhikode", 11.25, 75.77], ["Malappuram", 11.04, 76.08],
        ["Palakkad", 10.78, 76.65], ["Pathanamthitta", 9.27, 76.79],
        ["Thiruvananthapuram", 8.52, 76.94], ["Thrissur", 10.52, 76.21],
        ["Wayanad", 11.69, 76.08]
    ],
    "Madhya Pradesh": [
        ["Agar Malwa", 23.71, 76.02], ["Alirajpur", 22.30, 74.35], ["Anuppur", 23.10, 81.69],
        ["Ashoknagar", 24.58, 77.73], ["Balaghat", 21.81, 80.19], ["Barwani", 22.03, 74.90],
        ["Betul", 21.90, 77.90], ["Bhind", 26.56, 78.78], ["Bhopal", 23.26, 77.41],
        ["Burhanpur", 21.31, 76.23], ["Chhatarpur", 24.92, 79.59], ["Chhindwara", 22.06, 78.93],
        ["Damoh", 23.84, 79.44], ["Datia", 25.67, 78.46], ["Dewas", 22.97, 76.05],
        ["Dhar", 22.60, 75.30], ["Dindori", 22.95, 81.08], ["Guna", 24.65, 77.31],
        ["Gwalior", 26.22, 78.18], ["Harda", 22.34, 77.10], ["Hoshangabad", 22.75, 77.73],
        ["Indore", 22.72, 75.86], ["Jabalpur", 23.17, 79.93], ["Jhabua", 22.77, 74.60],
        ["Katni", 23.83, 80.40], ["Khandwa", 21.82, 76.35], ["Khargone", 21.83, 75.62],
        ["Mandla", 22.60, 80.38], ["Mandsaur", 24.07, 75.07], ["Morena", 26.50, 77.99],
        ["Narsinghpur", 22.95, 79.19], ["Neemuch", 24.47, 74.87], ["Panna", 24.72, 80.19],
        ["Raisen", 23.33, 77.79], ["Rajgarh", 24.01, 76.62], ["Ratlam", 23.33, 75.04],
        ["Rewa", 24.53, 81.30], ["Sagar", 23.84, 78.74], ["Satna", 24.58, 80.83],
        ["Sehore", 23.20, 77.08], ["Seoni", 22.08, 79.55], ["Shahdol", 23.30, 81.35],
        ["Shajapur", 23.43, 76.27], ["Sheopur", 25.67, 76.70], ["Shivpuri", 25.43, 77.66],
        ["Sidhi", 24.42, 81.88], ["Singrauli", 24.20, 82.67], ["Tikamgarh", 24.74, 78.83],
        ["Ujjain", 23.18, 75.77], ["Umaria", 23.52, 80.83], ["Vidisha", 23.53, 77.80],
        ["Niwari", 25.13, 78.83], ["Mauganj", 24.67, 81.88],
        ["Maihar", 24.26, 80.76], ["Chachaura", 24.45, 76.77],
        ["Nagda", 23.45, 75.42], ["Pandhurna", 21.60, 78.52]
    ],
    "Maharashtra": [
        ["Ahmednagar", 19.09, 74.74], ["Akola", 20.71, 77.00], ["Amravati", 20.93, 77.75],
        ["Aurangabad", 19.88, 75.34], ["Beed", 18.99, 75.76], ["Bhandara", 21.17, 79.65],
        ["Buldhana", 20.53, 76.18], ["Chandrapur", 19.97, 79.30], ["Dhule", 20.90, 74.78],
        ["Gadchiroli", 20.18, 80.00], ["Gondia", 21.46, 80.20], ["Hingoli", 19.72, 77.15],
        ["Jalgaon", 21.01, 75.57], ["Jalna", 19.84, 75.88], ["Kolhapur", 16.70, 74.24],
        ["Latur", 18.40, 76.57], ["Mumbai City", 18.98, 72.84], ["Mumbai Suburban", 19.13, 72.85],
        ["Nagpur", 21.15, 79.09], ["Nanded", 19.16, 77.30], ["Nandurbar", 21.37, 74.24],
        ["Nashik", 20.00, 73.78], ["Osmanabad", 18.18, 76.04], ["Palghar", 19.69, 72.77],
        ["Parbhani", 19.27, 76.78], ["Pune", 18.52, 73.86], ["Raigad", 18.52, 73.13],
        ["Ratnagiri", 16.99, 73.30], ["Sangli", 16.85, 74.56], ["Satara", 17.68, 74.00],
        ["Sindhudurg", 16.35, 73.65], ["Solapur", 17.66, 75.91], ["Thane", 19.22, 73.17],
        ["Wardha", 20.74, 78.60], ["Washim", 20.11, 77.13], ["Yavatmal", 20.39, 78.12]
    ],
    "Manipur": [
        ["Bishnupur", 24.62, 93.78], ["Chandel", 24.33, 94.03], ["Churachandpur", 24.33, 93.68],
        ["Imphal East", 24.82, 94.00], ["Imphal West", 24.81, 93.93], ["Jiribam", 24.80, 93.12],
        ["Kakching", 24.50, 93.98], ["Kamjong", 25.54, 94.47], ["Kangpokpi", 25.13, 93.97],
        ["Noney", 25.02, 93.48], ["Pherzawl", 24.52, 93.33], ["Senapati", 25.27, 94.02],
        ["Tamenglong", 24.98, 93.52], ["Tengnoupal", 24.15, 94.12],
        ["Thoubal", 24.63, 94.02], ["Ukhrul", 25.12, 94.37]
    ],
    "Meghalaya": [
        ["East Garo Hills", 25.72, 90.58], ["East Jaintia Hills", 25.35, 92.43],
        ["East Khasi Hills", 25.57, 91.88], ["North Garo Hills", 25.95, 90.62],
        ["Ri Bhoi", 25.88, 91.88], ["South Garo Hills", 25.30, 90.60],
        ["South West Garo Hills", 25.37, 90.22], ["South West Khasi Hills", 25.42, 91.25],
        ["West Garo Hills", 25.52, 90.22], ["West Jaintia Hills", 25.45, 92.22],
        ["West Khasi Hills", 25.55, 91.28], ["Eastern West Khasi Hills", 25.52, 91.52]
    ],
    "Mizoram": [
        ["Aizawl", 23.73, 92.72], ["Champhai", 23.47, 93.33], ["Hnahthial", 22.37, 92.83],
        ["Khawzawl", 23.35, 93.17], ["Kolasib", 24.22, 92.68], ["Lawngtlai", 22.42, 92.90],
        ["Lunglei", 22.88, 92.75], ["Mamit", 23.92, 92.48], ["Saiha", 22.48, 92.97],
        ["Saitual", 23.83, 92.92], ["Serchhip", 23.30, 92.85]
    ],
    "Nagaland": [
        ["Chumoukedima", 25.87, 93.73], ["Dimapur", 25.87, 93.73], ["Kiphire", 25.97, 95.15],
        ["Kohima", 25.67, 94.12], ["Longleng", 26.27, 94.72], ["Mokokchung", 26.32, 94.52],
        ["Mon", 26.72, 95.00], ["Niuland", 25.78, 93.85], ["Noklak", 26.42, 95.05],
        ["Peren", 25.52, 93.73], ["Phek", 25.67, 94.47], ["Shamator", 26.08, 95.15],
        ["Tseminyu", 25.90, 94.00], ["Tuensang", 26.27, 94.83], ["Wokha", 26.10, 94.27],
        ["Zunheboto", 25.97, 94.52]
    ],
    "Odisha": [
        ["Angul", 20.84, 85.10], ["Balangir", 20.72, 83.49], ["Balasore", 21.49, 86.93],
        ["Bargarh", 21.33, 83.62], ["Bhadrak", 21.05, 86.50], ["Boudh", 20.84, 84.32],
        ["Cuttack", 20.46, 85.88], ["Deogarh", 21.54, 84.73], ["Dhenkanal", 20.67, 85.60],
        ["Gajapati", 19.22, 84.13], ["Ganjam", 19.60, 84.40], ["Jagatsinghpur", 20.26, 86.17],
        ["Jajpur", 20.84, 86.33], ["Jharsuguda", 21.85, 84.01], ["Kalahandi", 19.91, 83.17],
        ["Kandhamal", 20.30, 84.23], ["Kendrapara", 20.50, 86.42], ["Kendujhar", 21.63, 85.58],
        ["Khordha", 20.18, 85.62], ["Koraput", 18.81, 82.72], ["Malkangiri", 18.35, 81.88],
        ["Mayurbhanj", 21.94, 86.73], ["Nabarangpur", 19.23, 82.55], ["Nayagarh", 20.13, 85.10],
        ["Nuapada", 20.78, 82.55], ["Puri", 19.81, 85.83], ["Rayagada", 19.17, 83.42],
        ["Sambalpur", 21.47, 83.97], ["Subarnapur", 20.83, 83.87], ["Sundargarh", 22.12, 84.04]
    ],
    "Punjab": [
        ["Amritsar", 31.63, 74.87], ["Barnala", 30.38, 75.55], ["Bathinda", 30.21, 74.95],
        ["Faridkot", 30.67, 74.76], ["Fatehgarh Sahib", 30.64, 76.39],
        ["Fazilka", 30.40, 74.03], ["Ferozepur", 30.93, 74.61], ["Gurdaspur", 32.04, 75.41],
        ["Hoshiarpur", 31.53, 75.91], ["Jalandhar", 31.33, 75.57], ["Kapurthala", 31.38, 75.38],
        ["Ludhiana", 30.90, 75.86], ["Malerkotla", 30.53, 75.88], ["Mansa", 29.99, 75.40],
        ["Moga", 30.82, 75.17], ["Pathankot", 32.27, 75.65], ["Patiala", 30.34, 76.39],
        ["Rupnagar", 30.97, 76.52], ["SAS Nagar", 30.70, 76.72], ["Sangrur", 30.24, 75.84],
        ["SBS Nagar", 31.12, 76.12], ["Sri Muktsar Sahib", 30.47, 74.51],
        ["Tarn Taran", 31.45, 74.93]
    ],
    "Rajasthan": [
        ["Ajmer", 26.45, 74.64], ["Alwar", 27.56, 76.63], ["Banswara", 23.55, 74.44],
        ["Baran", 25.10, 76.51], ["Barmer", 25.75, 71.39], ["Bharatpur", 27.22, 77.49],
        ["Bhilwara", 25.35, 74.63], ["Bikaner", 28.02, 73.31], ["Bundi", 25.44, 75.64],
        ["Chittorgarh", 24.88, 74.63], ["Churu", 28.29, 74.97], ["Dausa", 26.89, 76.34],
        ["Dholpur", 26.70, 77.90], ["Dungarpur", 23.84, 73.71], ["Hanumangarh", 29.58, 74.33],
        ["Jaipur", 26.92, 75.79], ["Jaisalmer", 26.92, 70.91], ["Jalore", 25.35, 72.62],
        ["Jhalawar", 24.60, 76.17], ["Jhunjhunu", 28.13, 75.40], ["Jodhpur", 26.24, 73.02],
        ["Karauli", 26.50, 77.02], ["Kota", 25.18, 75.83], ["Nagaur", 27.20, 73.73],
        ["Pali", 25.77, 73.32], ["Pratapgarh", 24.03, 74.78], ["Rajsamand", 25.07, 73.88],
        ["Sawai Madhopur", 26.02, 76.35], ["Sikar", 27.61, 75.14], ["Sirohi", 24.88, 72.86],
        ["Sri Ganganagar", 29.91, 73.88], ["Tonk", 26.17, 75.79], ["Udaipur", 24.58, 73.68],
        ["Anupgarh", 29.18, 73.21], ["Balotra", 25.83, 72.24], ["Beawar", 26.10, 74.32],
        ["Deeg", 27.47, 77.33], ["Didwana-Kuchaman", 27.40, 74.58], ["Dudu", 26.52, 75.39],
        ["Gangapur City", 26.47, 76.72], ["Jaipur Rural", 26.80, 75.90],
        ["Jodhpur Rural", 26.30, 73.10], ["Kekri", 25.97, 75.15], ["Khairthal-Tijara", 27.80, 76.65],
        ["Kotputli-Behror", 27.70, 76.20], ["Neem Ka Thana", 27.73, 75.79],
        ["Phalodi", 27.13, 72.37], ["Salumbar", 24.10, 74.05], ["Sanchore", 24.75, 71.77],
        ["Shahpura", 25.62, 74.93]
    ],
    "Sikkim": [
        ["East Sikkim", 27.33, 88.62], ["North Sikkim", 27.67, 88.53],
        ["South Sikkim", 27.15, 88.32], ["West Sikkim", 27.23, 88.18],
        ["Pakyong", 27.23, 88.72], ["Soreng", 27.15, 88.08]
    ],
    "Tamil Nadu": [
        ["Ariyalur", 11.14, 79.08], ["Chengalpattu", 12.69, 79.98],
        ["Chennai", 13.08, 80.27], ["Coimbatore", 11.00, 76.96],
        ["Cuddalore", 11.75, 79.77], ["Dharmapuri", 12.13, 78.16],
        ["Dindigul", 10.37, 77.97], ["Erode", 11.34, 77.72],
        ["Kallakurichi", 11.74, 78.96], ["Kancheepuram", 12.83, 79.70],
        ["Kanyakumari", 8.08, 77.57], ["Karur", 10.96, 78.08],
        ["Krishnagiri", 12.52, 78.21], ["Madurai", 9.93, 78.12],
        ["Mayiladuthurai", 11.10, 79.65], ["Nagapattinam", 10.77, 79.84],
        ["Namakkal", 11.22, 78.17], ["Nilgiris", 11.41, 76.73],
        ["Perambalur", 11.23, 78.88], ["Pudukkottai", 10.38, 78.82],
        ["Ramanathapuram", 9.37, 78.83], ["Ranipet", 12.93, 79.33],
        ["Salem", 11.65, 78.16], ["Sivaganga", 10.14, 78.48],
        ["Tenkasi", 8.96, 77.31], ["Thanjavur", 10.79, 79.14],
        ["Theni", 10.01, 77.48], ["Thoothukudi", 8.76, 78.13],
        ["Tiruchirappalli", 10.79, 78.69], ["Tirunelveli", 8.73, 77.70],
        ["Tirupathur", 12.50, 78.57], ["Tiruppur", 11.11, 77.35],
        ["Tiruvallur", 13.14, 79.91], ["Tiruvannamalai", 12.23, 79.07],
        ["Tiruvarur", 10.77, 79.64], ["Vellore", 12.92, 79.13],
        ["Viluppuram", 11.94, 79.49], ["Virudhunagar", 9.59, 77.96]
    ],
    "Telangana": [
        ["Adilabad", 19.67, 78.53], ["Bhadradri Kothagudem", 17.55, 80.62],
        ["Hyderabad", 17.39, 78.49], ["Jagtial", 18.79, 78.91],
        ["Jangaon", 17.73, 79.18], ["Jayashankar Bhupalpally", 18.43, 79.93],
        ["Jogulamba Gadwal", 16.23, 77.80], ["Kamareddy", 18.32, 78.34],
        ["Karimnagar", 18.44, 79.13], ["Khammam", 17.25, 80.15],
        ["Kumuram Bheem Asifabad", 19.36, 79.28], ["Mahabubabad", 17.60, 80.00],
        ["Mahabubnagar", 16.74, 78.00], ["Mancherial", 18.87, 79.43],
        ["Medak", 18.05, 78.26], ["Medchal-Malkajgiri", 17.53, 78.58],
        ["Mulugu", 18.19, 80.53], ["Nagarkurnool", 16.48, 78.32],
        ["Nalgonda", 17.05, 79.27], ["Narayanpet", 16.75, 77.50],
        ["Nirmal", 19.10, 78.35], ["Nizamabad", 18.67, 78.09],
        ["Peddapalli", 18.62, 79.38], ["Rajanna Sircilla", 18.38, 78.83],
        ["Rangareddy", 17.23, 78.25], ["Sangareddy", 17.62, 78.08],
        ["Siddipet", 18.10, 78.85], ["Suryapet", 17.14, 79.63],
        ["Vikarabad", 17.34, 77.90], ["Wanaparthy", 16.36, 78.07],
        ["Warangal", 17.97, 79.60], ["Yadadri Bhuvanagiri", 17.28, 78.95],
        ["Hanumakonda", 18.00, 79.55]
    ],
    "Tripura": [
        ["Dhalai", 24.00, 91.98], ["Gomati", 23.52, 91.47], ["Khowai", 24.07, 91.60],
        ["North Tripura", 24.32, 92.02], ["Sepahijala", 23.57, 91.28],
        ["South Tripura", 23.35, 91.48], ["Unakoti", 24.32, 92.10],
        ["West Tripura", 23.83, 91.28]
    ],
    "Uttar Pradesh": [
        ["Agra", 27.18, 78.02], ["Aligarh", 27.88, 78.08], ["Ambedkar Nagar", 26.44, 82.67],
        ["Amethi", 26.15, 81.81], ["Amroha", 28.90, 78.47], ["Auraiya", 26.47, 79.51],
        ["Ayodhya", 26.80, 82.20], ["Azamgarh", 26.07, 83.19], ["Baghpat", 28.95, 77.22],
        ["Bahraich", 27.57, 81.60], ["Ballia", 25.76, 84.15], ["Balrampur", 27.43, 82.17],
        ["Banda", 25.48, 80.34], ["Barabanki", 26.93, 81.19], ["Bareilly", 28.37, 79.42],
        ["Basti", 26.79, 82.76], ["Bhadohi", 25.40, 82.57], ["Bijnor", 29.37, 78.13],
        ["Budaun", 28.04, 79.13], ["Bulandshahr", 28.41, 77.85], ["Chandauli", 25.27, 83.27],
        ["Chitrakoot", 25.20, 80.85], ["Deoria", 26.50, 83.78], ["Etah", 27.56, 78.66],
        ["Etawah", 26.78, 79.02], ["Farrukhabad", 27.39, 79.58], ["Fatehpur", 25.93, 80.81],
        ["Firozabad", 27.15, 78.39], ["Gautam Buddh Nagar", 28.57, 77.32],
        ["Ghaziabad", 28.67, 77.42], ["Ghazipur", 25.58, 83.58], ["Gonda", 27.13, 81.97],
        ["Gorakhpur", 26.76, 83.37], ["Hamirpur", 25.96, 80.15], ["Hapur", 28.73, 77.78],
        ["Hardoi", 27.40, 80.13], ["Hathras", 27.60, 78.05], ["Jalaun", 26.15, 79.34],
        ["Jaunpur", 25.75, 82.68], ["Jhansi", 25.45, 78.57], ["Kannauj", 27.06, 79.91],
        ["Kanpur Dehat", 26.43, 79.78], ["Kanpur Nagar", 26.45, 80.35],
        ["Kasganj", 27.81, 78.65], ["Kaushambi", 25.53, 81.38], ["Kushinagar", 26.74, 83.89],
        ["Lakhimpur Kheri", 27.94, 80.78], ["Lalitpur", 24.69, 78.42],
        ["Lucknow", 26.85, 80.95], ["Maharajganj", 27.12, 83.56], ["Mahoba", 25.29, 79.87],
        ["Mainpuri", 27.23, 79.02], ["Mathura", 27.49, 77.67], ["Mau", 25.94, 83.56],
        ["Meerut", 28.98, 77.70], ["Mirzapur", 25.15, 82.57], ["Moradabad", 28.83, 78.77],
        ["Muzaffarnagar", 29.47, 77.70], ["Pilibhit", 28.64, 79.80],
        ["Pratapgarh", 25.90, 81.95], ["Prayagraj", 25.43, 81.85], ["Raebareli", 26.23, 81.24],
        ["Rampur", 28.80, 79.03], ["Saharanpur", 29.96, 77.55], ["Sambhal", 28.58, 78.57],
        ["Sant Kabir Nagar", 26.79, 83.07], ["Shahjahanpur", 27.88, 79.91],
        ["Shamli", 29.45, 77.32], ["Shrawasti", 27.50, 81.75], ["Siddharthnagar", 27.30, 83.09],
        ["Sitapur", 27.57, 80.68], ["Sonbhadra", 24.69, 83.07], ["Sultanpur", 26.27, 82.07],
        ["Unnao", 26.55, 80.49], ["Varanasi", 25.32, 83.01]
    ],
    "Uttarakhand": [
        ["Almora", 29.60, 79.66], ["Bageshwar", 29.84, 79.77], ["Chamoli", 30.40, 79.32],
        ["Champawat", 29.34, 80.09], ["Dehradun", 30.32, 78.03], ["Haridwar", 29.95, 78.16],
        ["Nainital", 29.38, 79.46], ["Pauri Garhwal", 30.15, 78.77],
        ["Pithoragarh", 29.58, 80.22], ["Rudraprayag", 30.28, 78.98],
        ["Tehri Garhwal", 30.39, 78.48], ["Udham Singh Nagar", 28.99, 79.41],
        ["Uttarkashi", 30.73, 78.45]
    ],
    "West Bengal": [
        ["Alipurduar", 26.49, 89.52], ["Bankura", 23.23, 87.07], ["Birbhum", 23.86, 87.62],
        ["Cooch Behar", 26.32, 89.45], ["Dakshin Dinajpur", 25.18, 88.77],
        ["Darjeeling", 27.04, 88.26], ["Hooghly", 22.91, 88.39], ["Howrah", 22.59, 88.31],
        ["Jalpaiguri", 26.52, 88.73], ["Jhargram", 22.45, 86.99], ["Kalimpong", 27.06, 88.47],
        ["Kolkata", 22.57, 88.36], ["Malda", 25.01, 88.14],
        ["Murshidabad", 24.18, 88.27], ["Nadia", 23.47, 88.56],
        ["North 24 Parganas", 22.62, 88.44], ["Paschim Bardhaman", 23.24, 87.07],
        ["Paschim Medinipur", 22.42, 87.32], ["Purba Bardhaman", 23.23, 87.85],
        ["Purba Medinipur", 22.28, 87.92], ["Purulia", 23.33, 86.37],
        ["South 24 Parganas", 22.16, 88.44], ["Uttar Dinajpur", 26.12, 88.17]
    ],

    # ── Union Territories ─────────────────────────────────────
    "Delhi": [
        ["Central Delhi", 28.65, 77.23], ["East Delhi", 28.63, 77.30],
        ["New Delhi", 28.61, 77.20], ["North Delhi", 28.72, 77.20],
        ["North East Delhi", 28.69, 77.27], ["North West Delhi", 28.73, 77.10],
        ["Shahdara", 28.67, 77.29], ["South Delhi", 28.53, 77.23],
        ["South East Delhi", 28.55, 77.27], ["South West Delhi", 28.55, 77.07],
        ["West Delhi", 28.63, 77.10]
    ],
    "Jammu and Kashmir": [
        ["Anantnag", 33.73, 75.15], ["Bandipora", 34.42, 74.65], ["Baramulla", 34.20, 74.34],
        ["Budgam", 34.03, 74.72], ["Doda", 33.15, 75.55], ["Ganderbal", 34.23, 74.78],
        ["Jammu", 32.73, 74.87], ["Kathua", 32.39, 75.52], ["Kishtwar", 33.31, 75.77],
        ["Kulgam", 33.64, 75.02], ["Kupwara", 34.53, 74.25], ["Poonch", 33.77, 74.10],
        ["Pulwama", 33.87, 74.90], ["Rajouri", 33.38, 74.31], ["Ramban", 33.24, 75.23],
        ["Reasi", 33.08, 74.83], ["Samba", 32.56, 75.12], ["Shopian", 33.72, 74.83],
        ["Srinagar", 34.08, 74.79], ["Udhampur", 32.93, 75.14]
    ],
    "Ladakh": [
        ["Kargil", 34.55, 76.13], ["Leh", 34.17, 77.58]
    ],
    "Puducherry": [
        ["Puducherry", 11.94, 79.83], ["Karaikal", 10.92, 79.84],
        ["Mahe", 11.70, 75.54], ["Yanam", 16.73, 82.22]
    ],
    "Chandigarh": [
        ["Chandigarh", 30.73, 76.78]
    ],
    "Andaman and Nicobar Islands": [
        ["Nicobar", 7.13, 93.77], ["North and Middle Andaman", 12.80, 92.87],
        ["South Andaman", 11.62, 92.72]
    ],
    "Dadra and Nagar Haveli and Daman and Diu": [
        ["Dadra and Nagar Haveli", 20.27, 73.01], ["Daman", 20.41, 72.84],
        ["Diu", 20.71, 70.99]
    ],
    "Lakshadweep": [
        ["Lakshadweep", 10.57, 72.64]
    ]
}


def generate():
    """Generate the districts.json file."""
    districts = []

    for state, entries in DISTRICTS_DATA.items():
        for entry in entries:
            districts.append({
                "state": state,
                "district": entry[0],
                "lat": entry[1],
                "lng": entry[2]
            })

    output_path = Path(__file__).parent / "districts.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(districts, f, ensure_ascii=False, indent=2)

    # Print summary
    print(f"✓ Generated {output_path}")
    print(f"  Total districts: {len(districts)}")
    print(f"  States/UTs covered: {len(DISTRICTS_DATA)}")
    print(f"\n  Per-state count:")
    for state, entries in sorted(DISTRICTS_DATA.items()):
        print(f"    {state:45s} {len(entries):3d} districts")


if __name__ == "__main__":
    generate()
