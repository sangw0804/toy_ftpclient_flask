def ls_trim(ls):
  ls = map(lambda l: l.split(), ls)

  new_ls = []
  for l in ls:
    new_l = {}
    new_l['is_d'] = (l[0][0] == 'd')
    new_l['desc'] = ' '.join(l[0:-1])
    new_l['name'] = l[-1]
    new_ls.append(new_l)
  
  return new_ls