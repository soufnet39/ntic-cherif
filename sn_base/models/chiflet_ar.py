v1=["","واحد ","إثنان ","ثلاثة ","أربعة ","خمسة ","ستة ","سبعة ","ثمانية ","تسعة "]
v2=["","إحدى ","إثنا ","ثلاثة ","أربعة ","خمسة ","ستة ","سبعة ","ثمانية ","تسعة "]
v3=["","عشرة ","عشرون ","ثلاثون ","أربعون ","خمسون ","ستون ","سبعون ","ثمانون ","تسعون "]
v4=["","مائة ","مائتان ","ثلاثمائة ","أربعمائة ","خمسمائة ","ستمائة ","سبعمائة ","ثمانمائة ","تسعمائة "]
v5=["إثنان","ألفان","مليونان","ملياران"]
v6=["","آلاف ","ملايين ","ملايير "]
v7=["واحد","ألف ","مليون  ","مليار "]

################################
def chiflet(vl):
################################

   if vl==0.0:
      return "صفر دينار جزائري "
   if vl==1.0:
      return "دينار جزائري واحد"
   vl = str(vl).strip()
   vm = vl
   vv = ""
   pos = vl.find(".")
   if (pos > -1):
      vm = vl[0:pos]
      vv = vl[pos + 1 :]

   vm = vm.zfill(12)  # 000000001234 => 12
   vv = vv.zfill(3)  # 000 => 3
   cp=''
   for i in range(4):
      pvm = vm[i * 3 : i * 3 + 3]
      mrc = morso(pvm,i)
      cp += (' و' if (cp and mrc) else '') + mrc
   cp += " دينار جزائري "
   if vv!="000":
      cp += ' و'+ morso(vv,3)+" سنتيم "


   return cp

#####################################
def morso(pvm,i):
   cp=''
   if int(pvm) == 0:
      return cp
   if int(pvm) == 1:
      cp +=   v7[3 - i]
      return cp
   if int(pvm) == 2:
      cp +=  v5[3 - i]
      return cp

   md3 =pvm[0:1]
   md2 =pvm[1:2]
   md1 = pvm[2:3]
   acharat = (md2 == '1')
   achara = (int(md2+md1) == 10)

   if (md3 != "0"):
      cp += (' و' if (cp) else '') + v4[int(md3)]
   if (md2 != "0" and md1 == "0"):
      cp += (' و' if (cp) else '') + v3[int(md2)]
   if (md2 == "1" and md1 != "0"):
      cp += (' و' if (cp) else '') + v2[int(md1)] + 'عشر '
   else:
      if (md2 != "0" and md1 != "0"):
         cp += (' و' if (cp) else '') + v2[int(md1)] + (" " if acharat else " و") + v3[int(md2)]
      if (md2 == "0" and md1 != "0"):
         cp += (' و' if (cp) else '') + v1[int(md1)]
   if (acharat and not achara and i < 3):
      cp += v7[3 - i]  + "ا "
   else:
      if i < 3:
         cp += v6[3-i] if (int(pvm)<11) else v7[3-i]  # unity


   return cp
