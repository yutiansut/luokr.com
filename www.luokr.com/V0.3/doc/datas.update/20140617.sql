update alogs set alog_data=substr(alog_text, instr(alog_text, x'0a')+1) where instr(alog_text, x'0a')
update alogs set alog_text=substr(alog_text, 0, instr(alog_text, x'0a')) where instr(alog_text, x'0a')
