package com.ipedg.minecraft;

import com.comphenix.protocol.utility.StreamSerializer;
import org.bukkit.Bukkit;
import org.bukkit.Material;
import org.bukkit.command.Command;
import org.bukkit.command.CommandSender;
import org.bukkit.command.ConsoleCommandSender;
import org.bukkit.entity.Player;
import org.bukkit.inventory.ItemStack;
import org.bukkit.plugin.java.JavaPlugin;

import java.io.*;

public class SaveItem extends JavaPlugin {
    @Override
    public void onEnable() {
        if (!getDataFolder().exists()) {
            getDataFolder().mkdir();
        }
        File file = new File(getDataFolder(),"config.yml");
        if (!(file.exists())){
            saveDefaultConfig();
        }
        super.onEnable();
    }

    public static ItemStack getItemStack(String data)
    {
        StreamSerializer ss=new StreamSerializer();
        try
        {
            return ss.deserializeItemStack(data);
        }catch(Exception e){e.printStackTrace();}
        return null;
    }
    public static String toData(ItemStack item)
    {
        StreamSerializer ss=new StreamSerializer();
        try
        {
            return ss.serializeItemStack(item);
        }catch(Exception e){e.printStackTrace();}
        return null;
    }



    public void CreateItem(String ItemName,String Data){
        File file = new File(getDataFolder() + File.separator + ItemName+".Fuck");
        if (!file.exists()){
            try{
                file.createNewFile();
                FileWriter fileWritter = new FileWriter(file,true);
                fileWritter.write(Data);
                fileWritter.close();
            }catch (IOException e){
                e.printStackTrace();
            }
        }
    }


    public String ReadFile(String ItemName){
        File file = new File(getDataFolder() + File.separator + ItemName+".Fuck");
        try{
            FileInputStream fis=new FileInputStream(file);
            byte[] b=new byte[fis.available()];//新建一个字节数组
            fis.read(b);//将文件中的内容读取到字节数组中
            fis.close();
            String str2=new String(b);//再将字节数组中的内容转化成字符串形式输出
            return str2;
        }catch (IOException e){
            e.printStackTrace();
        }
        return "";

    }

    @Override
    public boolean onCommand(CommandSender sender, Command command, String label, String[] args) {
        if (sender instanceof Player &&sender.isOp()){
            Player player = (Player) sender;
            if (args.length==2){
                if (args[0].equalsIgnoreCase("save")){
                    ItemStack itemInHand = player.getItemInHand();
                    if (itemInHand!=null&&itemInHand.getType()!= Material.AIR){
                        String s = toData(itemInHand);
                        System.out.print(s.length());
                        CreateItem(args[1],s);
                    }
                }
            }else if (args.length==3){
                if (args[0].equalsIgnoreCase("give")){
                    String filename = args[1];
                    String playername = args[2];
                    Player player1 = Bukkit.getServer().getPlayer(playername);
                    if (player1.isOnline()){
                        String s = ReadFile(filename);
                        if (!s.equals("")){
                            ItemStack itemStack = getItemStack(s);
                            player1.getInventory().addItem(itemStack);
                            player1.sendMessage("你得到了"+filename);
                        }else {
                            sender.sendMessage("没有这个物品");
                        }
                    }else {
                        sender.sendMessage("玩家不在线");
                    }
                }
            }
        }else if (sender.isOp()&&sender instanceof ConsoleCommandSender){
            if (args.length==3&&args[0].equalsIgnoreCase("give")){
                String filename = args[1];
                String playername = args[2];
                Player player1 = Bukkit.getServer().getPlayer(playername);
                if (player1.isOnline()){
                    String s = ReadFile(filename);
                    if (!s.equals("")){
                        ItemStack itemStack = getItemStack(s);
                        player1.getInventory().addItem(itemStack);
                        player1.sendMessage("你得到了"+filename);
                    }else {
                        sender.sendMessage("没有这个物品");
                    }
                }else {
                    sender.sendMessage("玩家不在线");
                }
            }
        }
        return super.onCommand(sender, command, label, args);
    }
}
