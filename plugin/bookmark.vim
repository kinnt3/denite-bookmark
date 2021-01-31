if exists('g:loaded_denite_bookmark')
  finish
endif
let g:loaded_denite_bookmark = 1

call denite#bookmark#init()
