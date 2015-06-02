  
my.wordlist = c("mywordlist-200fw.txt", "mywordlist-200cw.txt", "mywordlist-em.txt")

my.diagnostic.files = paste("diagno", my.wordlist, sep="_")

for (i in 1: length(my.wordlist)) { 
    
my.current.features = scan(my.wordlist[i], what="char", sep="\n")

results = stylo(corpus.dir="corpus", features = my.current.features, gui=FALSE, corpus.lang = "French.all", display.on.screen = FALSE, write.png.file = TRUE, plot.custom.height = 12, mfw.min = 200, mfw.max = 200, use.existing.freq.tables = FALSE)

#cat(file = my.diagnostic.files[i], results$features.actually.used, sep="\n")

cat(file = my.diagnostic.files[i], results$distance.table, sep="\n")


}




