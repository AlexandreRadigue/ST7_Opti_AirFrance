\ Model TD4-Exo2
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  4 x_0_1 + 5 x_0_2 + 9 x_0_3 + 5 x_1_4 + 3 x_1_5 + 8 x_2_4 + 6 x_2_5
   + 5 x_2_6 + 6 x_3_5 + 7 x_3_6 + 7 x_4_7 + 3 x_5_7 + 3 x_6_7
Subject To
 ConstrVertex0: x_0_1 + x_0_2 + x_0_3 = 1
 constr1: x_0_1 - x_1_4 - x_1_5 = 0
 constr2: x_0_2 - x_2_4 - x_2_5 - x_2_6 = 0
 constr3: x_0_3 - x_3_5 - x_3_6 = 0
 constr4: x_1_4 + x_2_4 - x_4_7 = 0
 constr5: x_1_5 + x_2_5 + x_3_5 - x_5_7 = 0
 constr6: x_2_6 + x_3_6 - x_6_7 = 0
Bounds
Binaries
 x_0_1 x_0_2 x_0_3 x_1_4 x_1_5 x_2_4 x_2_5 x_2_6 x_3_5 x_3_6 x_4_7 x_5_7
 x_6_7
End
