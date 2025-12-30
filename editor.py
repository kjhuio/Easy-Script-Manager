import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import customtkinter as ctk
from colorama import Fore, Style
import zipfile
import json
import os
import sys

# CustomTkinter設定
ctk.set_appearance_mode("dark")  # デフォルトはダークモード
ctk.set_default_color_theme("blue")

def resource_path(relative_path):
    """リソースファイルのパスを取得(exe化対応)"""
    try:
        # PyInstallerで作成されたexeの場合
        base_path = sys._MEIPASS
    except Exception:
        # 通常のPython実行の場合
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# 起動時のロゴ表示
def print_logo():
    print(f"{Fore.GREEN}█████ {Fore.RED} █████ {Fore.YELLOW} ██   ██")
    print(f"{Fore.GREEN}█     {Fore.RED} █    {Fore.YELLOW}  █ █ █ █")
    print(f"{Fore.GREEN}█████ {Fore.RED} █████ {Fore.YELLOW} █  █  █")
    print(f"{Fore.GREEN}█     {Fore.RED}     █ {Fore.YELLOW} █     █")
    print(f"{Fore.GREEN}█████ {Fore.RED} █████ {Fore.YELLOW} █     █")
    print(f"{Style.RESET_ALL}Easy Script Manager v0.1 beta")

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("ESM - Easy Script Manager")
        self.root.geometry("800x600")
        self.current_mode = "dark"  # 現在のモード
        try:
            icon_path = resource_path('logo.ico')
            self.root.iconbitmap(icon_path)
        except:
            pass
        self.show_top_screen()
    
    def show_top_screen(self):
        """トップ画面"""
        # 既存のウィジェットをクリア
        for widget in self.root.winfo_children():
            widget.destroy()
        
        frame = ctk.CTkFrame(self.root)
        frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # タイトルとモード切替
        header_frame = ctk.CTkFrame(frame, fg_color="transparent")
        header_frame.pack(pady=(20, 40), fill="x")
        
        ctk.CTkLabel(header_frame, text="ESM - Easy Script Manager", 
                    font=ctk.CTkFont(size=28, weight="bold")).pack()
        
        # モード切替スイッチ
        mode_frame = ctk.CTkFrame(frame, fg_color="transparent")
        mode_frame.pack(pady=(0, 20))
        
        ctk.CTkLabel(mode_frame, text="外観モード:", 
                    font=ctk.CTkFont(size=13)).pack(side="left", padx=5)
        
        mode_switch = ctk.CTkSegmentedButton(mode_frame, 
                                             values=["ダークモード", "ライトモード"],
                                             command=self.change_appearance_mode)
        mode_switch.pack(side="left", padx=5)
        mode_switch.set("ダークモード")  # デフォルト選択
        
        # メニューボタン
        ctk.CTkButton(frame, text="新規プロジェクト作成", width=300, height=50,
                     font=ctk.CTkFont(size=16),
                     command=self.create_new_project).pack(pady=15)
        ctk.CTkButton(frame, text="既存プロジェクトを開く", width=300, height=50,
                     font=ctk.CTkFont(size=16),
                     command=self.open_project).pack(pady=15)
        ctk.CTkButton(frame, text="終了", width=300, height=50,
                     font=ctk.CTkFont(size=16),
                     command=self.root.quit).pack(pady=15)
    
    def change_appearance_mode(self, mode):
        """外観モードを変更"""
        if mode == "ダークモード":
            ctk.set_appearance_mode("dark")
            self.current_mode = "dark"
        else:
            ctk.set_appearance_mode("light")
            self.current_mode = "light"
    
    def create_new_project(self):
        """新規プロジェクト作成"""
        NewProjectDialog(self.root, self)
    
    def open_project(self):
        """既存プロジェクトを開く"""
        filepath = filedialog.askopenfilename(
            filetypes=[("ESM Project", "*.esm"), ("All Files", "*.*")]
        )
        
        if filepath:
            self.open_editor(filepath)
    
    def open_editor(self, filepath):
        """エディタ画面を開く"""
        EditorWindow(self.root, filepath, self)

class NewProjectDialog:
    def __init__(self, root, main_window):
        self.root = root
        self.main_window = main_window
        self.characters = {}
        
        self.dialog = ctk.CTkToplevel(root)
        self.dialog.title("新規プロジェクト作成")
        self.dialog.geometry("600x500")
        self.dialog.grab_set()
        
        self.setup_ui()
    
    def setup_ui(self):
        """UI構築"""
        # メインフレーム
        main_frame = ctk.CTkFrame(self.dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # タイトル入力
        ctk.CTkLabel(main_frame, text="プロジェクトタイトル:", 
                    font=ctk.CTkFont(size=14)).pack(anchor="w", pady=(0, 5))
        self.title_entry = ctk.CTkEntry(main_frame, height=35)
        self.title_entry.pack(fill="x", pady=(0, 20))
        self.title_entry.insert(0, "新規プロジェクト")
        
        # キャラクター設定
        ctk.CTkLabel(main_frame, text="キャラクター設定", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", pady=(0, 10))
        
        # キャラクター一覧
        list_frame = ctk.CTkFrame(main_frame)
        list_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        self.char_listbox = tk.Listbox(list_frame, bg="#2b2b2b", fg="white", 
                                       selectbackground="#1f538d", font=("Arial", 11))
        self.char_listbox.pack(fill="both", expand=True, padx=10, pady=10)
        
        # キャラクター追加/削除ボタン
        btn_frame = ctk.CTkFrame(main_frame)
        btn_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkButton(btn_frame, text="キャラ追加", height=35,
                     command=self.add_character).pack(side="left", padx=5, expand=True, fill="x")
        ctk.CTkButton(btn_frame, text="キャラ削除", height=35,
                     command=self.delete_character).pack(side="left", padx=5, expand=True, fill="x")
        
        # 作成/キャンセルボタン
        bottom_frame = ctk.CTkFrame(main_frame)
        bottom_frame.pack(fill="x")
        
        ctk.CTkButton(bottom_frame, text="キャンセル", height=40,
                     command=self.dialog.destroy).pack(side="left", padx=5, expand=True, fill="x")
        ctk.CTkButton(bottom_frame, text="作成", height=40, fg_color="#2fa572",
                     hover_color="#28865f", command=self.create_project).pack(side="right", padx=5, expand=True, fill="x")
    
    def add_character(self):
        """キャラクター追加"""
        add_dialog = ctk.CTkToplevel(self.dialog)
        add_dialog.title("キャラクター追加")
        add_dialog.geometry("350x250")
        add_dialog.grab_set()
        
        frame = ctk.CTkFrame(add_dialog)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(frame, text="正式名称:", font=ctk.CTkFont(size=13)).pack(anchor="w", pady=(0, 5))
        full_name_entry = ctk.CTkEntry(frame, height=35)
        full_name_entry.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(frame, text="略称:", font=ctk.CTkFont(size=13)).pack(anchor="w", pady=(0, 5))
        short_name_entry = ctk.CTkEntry(frame, height=35)
        short_name_entry.pack(fill="x", pady=(0, 20))
        
        def on_ok():
            full_name = full_name_entry.get().strip()
            short_name = short_name_entry.get().strip()
            
            if not full_name or not short_name:
                messagebox.showwarning("警告", "両方入力してください")
                return
            
            if short_name in self.characters:
                messagebox.showwarning("警告", "この略称は既に使用されています")
                return
            
            self.characters[short_name] = full_name
            self.refresh_character_list()
            add_dialog.destroy()
        
        ctk.CTkButton(frame, text="追加", height=40, command=on_ok).pack(fill="x")
    
    def delete_character(self):
        """キャラクター削除"""
        selection = self.char_listbox.curselection()
        if not selection:
            messagebox.showwarning("警告", "削除するキャラクターを選択してください")
            return
        
        item = self.char_listbox.get(selection[0])
        short_name = item.split("(")[1].rstrip(")")
        
        if messagebox.askyesno("確認", f"{item} を削除しますか?"):
            del self.characters[short_name]
            self.refresh_character_list()
    
    def refresh_character_list(self):
        """キャラクターリストを更新"""
        self.char_listbox.delete(0, tk.END)
        for short_name, full_name in self.characters.items():
            self.char_listbox.insert(tk.END, f"{full_name}({short_name})")
    
    def create_project(self):
        """プロジェクトを作成"""
        filepath = filedialog.asksaveasfilename(
            defaultextension=".esm",
            filetypes=[("ESM Project", "*.esm"), ("All Files", "*.*")]
        )
        
        if filepath:
            try:
                title = self.title_entry.get().strip()
                if not title:
                    title = "新規プロジェクト"
                
                project_data = {
                    "title": title,
                    "characters": self.characters
                }
                
                with zipfile.ZipFile(filepath, 'w') as z:
                    z.writestr('config.json', json.dumps(project_data, ensure_ascii=False, indent=2))
                    z.writestr('script.txt', '')
                    z.writestr('exported.txt', '')
                
                self.dialog.destroy()
                self.main_window.open_editor(filepath)
            except Exception as e:
                messagebox.showerror("エラー", f"プロジェクトの作成に失敗しました: {e}")

class EditorWindow:
    def __init__(self, root, filepath, main_window):
        self.root = root
        self.filepath = filepath
        self.main_window = main_window
        self.characters = {}
        
        # 既存のウィジェットをクリア
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # プロジェクトを読み込み
        self.load_project()
        
        # UIを構築
        self.setup_ui()
    
    def load_project(self):
        """プロジェクトファイルを読み込み"""
        try:
            with zipfile.ZipFile(self.filepath, 'r') as z:
                config_data = json.loads(z.read('config.json').decode('utf-8'))
                self.title = config_data.get('title', '無題')
                self.characters = config_data.get('characters', {})
                self.script_content = z.read('script.txt').decode('utf-8')
        except Exception as e:
            messagebox.showerror("エラー", f"プロジェクトの読み込みに失敗しました: {e}")
            self.title = "無題"
            self.characters = {}
            self.script_content = ""
    
    def setup_ui(self):
        """UI構築"""
        # グリッドの重み設定
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        
        # 上部: タイトル
        title_frame = ctk.CTkFrame(self.root)
        title_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        
        ctk.CTkLabel(title_frame, text="タイトル:", font=ctk.CTkFont(size=13)).pack(side="left", padx=(10, 5))
        self.title_entry = ctk.CTkEntry(title_frame, height=35)
        self.title_entry.insert(0, self.title)
        self.title_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # 左フレーム
        left_frame = ctk.CTkFrame(self.root, width=250)
        left_frame.grid(row=1, column=0, sticky="nsew", padx=(10, 5), pady=(0, 10))
        left_frame.grid_propagate(False)
        
        # 左上: キャラクター一覧
        char_frame = ctk.CTkFrame(left_frame)
        char_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(char_frame, text="キャラクター", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(5, 10))
        
        # Listbox (CustomTkinterにはListboxがないのでtkinter使用)
        listbox_bg = "#2b2b2b" if self.main_window.current_mode == "dark" else "#f0f0f0"
        listbox_fg = "white" if self.main_window.current_mode == "dark" else "black"
        self.char_listbox = tk.Listbox(char_frame, bg=listbox_bg, fg=listbox_fg,
                                       selectbackground="#1f538d", font=("Arial", 11))
        self.char_listbox.pack(fill="both", expand=True, padx=5, pady=(0, 10))
        
        # キャラクターを読み込み
        self.refresh_character_list()
        
        ctk.CTkButton(char_frame, text="キャラ追加", height=35,
                     command=self.add_character).pack(fill="x", padx=5, pady=2)
        ctk.CTkButton(char_frame, text="キャラ削除", height=35,
                     command=self.delete_character).pack(fill="x", padx=5, pady=2)
        
        # 左下: ボタン
        button_frame = ctk.CTkFrame(left_frame)
        button_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        ctk.CTkButton(button_frame, text="保存", height=40, fg_color="#2fa572",
                     hover_color="#28865f", command=self.save_project).pack(fill="x", pady=3)
        ctk.CTkButton(button_frame, text="エクスポート", height=40, fg_color="#1f538d",
                     hover_color="#163f6d", command=self.export_script).pack(fill="x", pady=3)
        ctk.CTkButton(button_frame, text="閉じる", height=40,
                     command=self.close_editor).pack(fill="x", pady=3)
        
        # 右: エディタ
        editor_frame = ctk.CTkFrame(self.root)
        editor_frame.grid(row=1, column=1, sticky="nsew", padx=(5, 10), pady=(0, 10))
        
        ctk.CTkLabel(editor_frame, text="原稿エディタ (略称:セリフ の形式で入力)",
                    font=ctk.CTkFont(size=13)).pack(anchor="w", padx=10, pady=(10, 5))
        
        # テキストエディタ (CustomTkinterのCTkTextboxを使用)
        self.editor = ctk.CTkTextbox(editor_frame, wrap="word", font=("Consolas", 12))
        self.editor.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.editor.insert("1.0", self.script_content)
    
    def refresh_character_list(self):
        """キャラクターリストを更新"""
        self.char_listbox.delete(0, tk.END)
        for short_name, full_name in self.characters.items():
            self.char_listbox.insert(tk.END, f"{full_name}({short_name})")
    
    def add_character(self):
        """キャラクター追加ダイアログ"""
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("キャラクター追加")
        dialog.geometry("350x250")
        dialog.grab_set()
        
        frame = ctk.CTkFrame(dialog)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(frame, text="正式名称:", font=ctk.CTkFont(size=13)).pack(anchor="w", pady=(0, 5))
        full_name_entry = ctk.CTkEntry(frame, height=35)
        full_name_entry.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(frame, text="略称:", font=ctk.CTkFont(size=13)).pack(anchor="w", pady=(0, 5))
        short_name_entry = ctk.CTkEntry(frame, height=35)
        short_name_entry.pack(fill="x", pady=(0, 20))
        
        def on_ok():
            full_name = full_name_entry.get().strip()
            short_name = short_name_entry.get().strip()
            
            if not full_name or not short_name:
                messagebox.showwarning("警告", "両方入力してください")
                return
            
            if short_name in self.characters:
                messagebox.showwarning("警告", "この略称は既に使用されています")
                return
            
            self.characters[short_name] = full_name
            self.refresh_character_list()
            dialog.destroy()
        
        ctk.CTkButton(frame, text="追加", height=40, command=on_ok).pack(fill="x")
    
    def delete_character(self):
        """選択したキャラクターを削除"""
        selection = self.char_listbox.curselection()
        if not selection:
            messagebox.showwarning("警告", "削除するキャラクターを選択してください")
            return
        
        item = self.char_listbox.get(selection[0])
        short_name = item.split("(")[1].rstrip(")")
        
        if messagebox.askyesno("確認", f"{item} を削除しますか?"):
            del self.characters[short_name]
            self.refresh_character_list()
    
    def save_project(self):
        """プロジェクトを保存"""
        try:
            title = self.title_entry.get()
            script = self.editor.get("1.0", "end-1c").strip()
            
            # 変換済みテキストを生成
            exported = self.convert_script(script)
            
            config_data = {
                "title": title,
                "characters": self.characters
            }
            
            with zipfile.ZipFile(self.filepath, 'w') as z:
                z.writestr('config.json', json.dumps(config_data, ensure_ascii=False, indent=2))
                z.writestr('script.txt', script)
                z.writestr('exported.txt', exported)
            
            messagebox.showinfo("成功", "保存しました")
        except Exception as e:
            messagebox.showerror("エラー", f"保存に失敗しました: {e}")
    
    def convert_script(self, script):
        """略称を正式名称に変換"""
        lines = script.split('\n')
        converted = []
        
        for line in lines:
            if ':' in line:
                parts = line.split(':', 1)
                short_name = parts[0].strip()
                dialogue = parts[1].strip() if len(parts) > 1 else ""
                
                if short_name in self.characters:
                    full_name = self.characters[short_name]
                    converted.append(f"{full_name}:{dialogue}")
                else:
                    converted.append(line)
            else:
                converted.append(line)
        
        return '\n'.join(converted)
    
    def export_script(self):
        """変換済みスクリプトをエクスポート"""
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text File", "*.txt"), ("All Files", "*.*")]
        )
        
        if filepath:
            try:
                script = self.editor.get("1.0", "end-1c").strip()
                exported = self.convert_script(script)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(exported)
                
                messagebox.showinfo("成功", "エクスポートしました")
            except Exception as e:
                messagebox.showerror("エラー", f"エクスポートに失敗しました: {e}")
    
    def close_editor(self):
        """エディタを閉じてトップ画面に戻る"""
        if messagebox.askyesno("確認", "保存せずに閉じますか?"):
            self.main_window.show_top_screen()

def main():
    print_logo()
    
    root = ctk.CTk()
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()