# already removed addresses and tel numbers by hand (latter only cause had to do former by hand)
# 0. check addresses, NHS numbers and post codes have been removed:
def open_txt_file(path_to_doc):
    with open(path_to_doc, 'r') as f:
        pt_txt = f.read()

    return pt_txt

regex = r"NHS"
regex2 = r"Address"
regex_postcode = r"([Gg][Ii][Rr] 0[Aa]{2})|((([A-Za-z][0-9]{1,2})|(([A-Za-z][A-Ha-hJ-Yj-y][0-9]{1,2})|(([A-Za-z][0-9][A-Za-z])|([A-Za-z][A-Ha-hJ-Yj-y][0-9][A-Za-z]?))))\s?[0-9][A-Za-z]{2})"

path_to_folder='L:\\word_docs\\DOCX_done\\4. anonymised_without_addresses_telephones_edited\\'


for txt_file in os.listdir(path_to_folder):
    path_to_doc = os.path.join(path_to_folder, txt_file)

    #open the file
    pt_txt = open_txt_file(path_to_doc)

    
    if re.search(regex1, pt_txt):
        print("{} NHS".format(txt_file))
    
    if re.search(regex2, pt_txt):
        print("{} Address".format(txt_file))
    
    if re.search(regex_postcode, pt_txt):
        post_code = re.search(regex_postcode, pt_txt)
        print("{} postcode? {}".format(txt_file, post_code.group()))

    else:
        continue

    # all done. see end of 2. word_Docx_done jupyter notebook



# 1. remove unicode invalid characters such as bullet points from word
    # \uf0ae\uf020, uf0b7,

# 2. normalise phrases/terms
    # change "º" to "no"
    # change "yo"|"years old"|"yrs.*"|"years"|"yr old"|"y.o."|\d\s?+y to "yrs-old"
    # \d//[day, wk, month, yr] to \d per [day,wk,month,yr]
    # men. > meningitis
    # FC, Feb.C\w,  > Febrile Convulsions
    # NAD > Normal
    # HS > Hippocampal sclerosis
    # Right = ['Right', r"\sR\s", "Rt"]
    # Normal = [r"\sN\s", ]
    # SGTCS = [secondary GTCS, 2GTCS
    # # > fracture. 
    # déjà vu = [de ja vu, deja vu, deja vue]
    # Handed: Right, Handed \s+ Right
    # semiology terms

# 3. save renamed files in a new folder with uuid_no