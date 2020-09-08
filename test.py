whole_output = []
for i in etap_power.train_data:
    data = etap_power.train_data[i]['Avg']
    whole_output.append(data)
    plt.plot(list(data))
plt.show()
#%%
whole_output=np.array(whole_output)
mn=whole_output.mean(axis=0)
s=whole_output.std(axis=0)
plt.plot(mn-s)
plt.plot(mn,color='black')
plt.plot(mn+s)
plt.show()
#%%
res=[]
for i in range(len(y_train)):
    res.append(y_train[i]-predicted[i])
res=np.array(res)

mn=res.mean(axis=0)
s=res.std(axis=0)
tstar = 1.984 #two sided t distribution 95% confidence interval for errors
CI_down = mn - s/np.sqrt(res.shape[0])
CI_up = mn + s/np.sqrt(res.shape[0])


plt.plot(mn-s)
plt.plot(mn,color='black')
plt.plot(mn+s)
plt.show()

#%%
for i in range(len(y_train)):
    plt.plot(y_train[i])
    plt.plot(predicted[i])
    plt.plot(predicted[i]+CI_down)
    plt.plot(predicted[i]+CI_up)
    plt.show()

